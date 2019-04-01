import requests
from jinja2 import Environment, FileSystemLoader
import os
import xml.dom.minidom
import json
import pprint
import xmltodict
import numpy as np
from functools import wraps, partial
import numpy as np
from timeinterval import start as setInterval


TEMPLATE_DIR = './templates/'
CONTROLLER = 'http://admin:admin@192.168.56.102:8181'
HEADERS = {
    'Content-type': 'application/xml',
    'Accept': 'application/xml',
}
MAX_TRANSFER_RATE = 1000
pp = pprint.pprint


def prettyResponse(func):
    """
    Decorator that makes response data more readable and inspectable
    1.  Add pretty print XML method
    2.  Convert data to dict object
    """
    @wraps(func)
    def innerFunc(*args, **kwargs):
        res = func(*args, **kwargs)
        res.prettyXML = partial(print, xml.dom.minidom.parseString(res.content).toprettyxml())
        res.data_dict = json.loads(json.dumps(xmltodict.parse(res.content)))
        return res
    return innerFunc

def printRequestURL(func):
    @wraps(func)
    def innerFunc(*args, **kwargs):
        res = func(*args, **kwargs)
        print(res.request.url)
        return res
    return innerFunc


def _addFlow(filename, **params):
    jinja_args = {k:params[k] for k in params if k not in ['node_id']}
    url_args =   {k:params[k] for k in params if k in ['node_id', 'table_id', 'flow_id']}

    url="{controller}/restconf/config/opendaylight-inventory:nodes/node/{node_id}/table/{table_id}"
    if url_args['flow_id'] is not None:
        url += '/flow/{flow_id}'
    res = requests.put(
        url = url.format(controller=CONTROLLER, **url_args),
        headers = HEADERS,
        data = _getData(filename, **jinja_args)
    )
    return res


def _getData(filename, **params):
    directory = os.path.join(TEMPLATE_DIR, 'addFlow/')
    file_loader = FileSystemLoader(directory)
    env = Environment(loader=file_loader)
    return env.get_template(filename).render(**params)


def forwardPacket(node_id, table_id, flow_id, ip_src, ip_dest, out_conn):
    return _addFlow('forwardPacket.jinja', **locals())

@printRequestURL
def forwardFrame(node_id, table_id, flow_id, eth_src, eth_dest, out_conn):
    return _addFlow('forwardFrame.jinja', **locals())


def dropPacket(node_id, table_id, flow_id, eth_src):
    return _addFlow('dropPacket.jinja', **locals())


def removeFlow(node_id, table_id, flow_id):
    url="{controller}/restconf/config/opendaylight-inventory:nodes/node/{node_id}/table/{table_id}/flow/{flow_id}/"
    res = requests.delete(
        url     = url.format(controller=CONTROLLER, **locals()),
        headers = HEADERS
    )
    return res


@prettyResponse
def getFlowStats(node_id, table_id=None, flow_id=None):
    url="{controller}/restconf/operational/opendaylight-inventory:nodes/node/{node_id}/"
    if table_id is not None:
        url += "table/{table_id}/"
    if flow_id is not None:
        url += "flow/{flow_id}/"
    res = requests.get(
        url     = url.format(controller=CONTROLLER, **locals()),
        headers = HEADERS
    )
    return res


def getLinkStats(node_id, conn_id):
    url="{controller}/restconf/operational/opendaylight-inventory:nodes/node/{node_id}/node-connector/{conn_id}"
    res = requests.get(
        url     = url.format(controller=CONTROLLER, **locals()),
        headers = HEADERS
    )
    data_dict = json.loads(json.dumps(xmltodict.parse(res.content)))
    data = data_dict['node-connector']['flow-capable-node-connector-statistics']
    transmitted = int(data['bytes']['transmitted'])
    duration = int(data['duration']['second'])

    return transmitted, duration



@prettyResponse
def topology():
    url="{controller}/restconf/operational/network-topology:network-topology"
    res = requests.get(
        url = url.format(controller=CONTROLLER),
        headers = HEADERS
    )
    return res


def extractNodesInfo(topo):
    hosts = {}
    switches = {}

    for node_data in topo['network-topology']['topology']['node']:
        node_id = node_data['node-id']
        if node_id.startswith('host'):
            host = hosts[node_id] = {}
            host['mac'] = node_data['addresses']['mac']
        else:
            switches[node_id] = {}

    for link_data in topo['network-topology']['topology']['link']:
        if link_data['link-id'].startswith('host'):
            host_id = link_data['source']['source-node']
            hosts[host_id]['switch_id'] = link_data['destination']['dest-node']
            hosts[host_id]['switch_connector'] = link_data['destination']['dest-tp']
        elif link_data['link-id'].find('host') == -1:
            source_node = link_data['source']['source-node']
            connector = link_data['source']['source-tp']
            dest_node = link_data['destination']['dest-node']
            switches[source_node][dest_node] = connector

    return hosts, switches


def  genWeightsGraph(switches):
    transmitted = np.zeros((len(switches), len(switches)), dtype=np.uint32)
    duration = np.zeros((len(switches), len(switches)), dtype=np.uint32)
    inv_keys = {v:k for k, v in enumerate(switches.keys())}

    while True:

        weights = np.full((len(switches), len(switches)), np.inf)
        np.fill_diagonal(weights, 0)

        for src, dests in switches.items():
            for dest, conn in dests.items():
                i_src, i_dest = inv_keys[src], inv_keys[dest]
                prev_trans, prev_dur = transmitted[i_src, i_dest], duration[i_src, i_dest]
                trans, dur = getLinkStats(src, conn)
                weight = (trans - prev_trans) / (dur - prev_dur)
                weight = weight / MAX_TRANSFER_RATE if weight < MAX_TRANSFER_RATE else 1

                weights[i_src, i_dest] = weight if weight < 0.5 else 1/(1.01 - weight)

                transmitted[i_src, i_dest] = trans
                duration[i_src, i_dest] = dur

        yield weights


def floydWarshall(weights):
    n = weights.shape[0]

    d = np.copy(weights)
    p = np.full((n, n), float('NaN'))
    for i in range(n):
        for j in range(n):
            if d[i, j] != 0 and d[i, j] != np.inf:
                p[i, j] = i

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i, j] > d[i, k] + d[k, j]:
                    d[i, j] = d[i, k] + d[k, j]
                    p[i, j] = p[k, j]

    return p


def genL2Routes():
    topo = topology().data_dict
    hosts, switches = extractNodesInfo(topo)
    w_iter = genWeightsGraph(switches)
    index_to_id = list(switches.keys())
    id_to_index = {v:k for k, v in enumerate(index_to_id)}

    for host_id, host_info in hosts.items():
        mac = host_info['mac']
        switch_id = host_info['switch_id']
        switch_connector = host_info['switch_connector']
        forwardFrame(switch_id, 0, 99, None, mac, switch_connector)

    while True:
        weights = next(w_iter)
        routing_table = floydWarshall(weights)
        is_processed = np.zeros(len(switches), dtype=bool)
        for src_id, src_info in hosts.items():
            src_mac = src_info['mac']
            src_switch_id = src_info['switch_id']
            src_switch_index = id_to_index[src_switch_id]
            for dest_id, dest_info in hosts.items():
                dest_mac = dest_info['mac']
                dest_switch_id = dest_info['switch_id']
                dest_switch_index = id_to_index[dest_switch_id]

                if dest_switch_index != src_switch_index:
                    trace = [src_switch_index, dest_switch_index]
                    while True:
                        prev = int(routing_table[trace[0], trace[1]])
                        if prev != src_switch_index:
                            trace.insert(1, prev)
                        else:
                            break
                    for i in range(len(trace) - 1):
                        cur_sw_id  = index_to_id[trace[i]]
                        next_sw_id = index_to_id[trace[i+1]]
                        connector = switches[cur_sw_id][next_sw_id]
                        forwardFrame(cur_sw_id, 0, 99, src_mac, dest_mac, connector)
        print("*** Routing success, continue after 5 seconds\n")
        yield

# if __name__ == '__main__':
#     t = genL2Routes()
#     setInterval(5000, partial(next, t))
