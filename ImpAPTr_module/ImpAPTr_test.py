<<<<<<< HEAD
import os

import numpy as np
import sys
# sys.path.append('E:/Documents/Desktop/test1')


sys.path.append(os.path.dirname(os.getcwd()))
from ImpAPTr_module import ImpAPTr

dimension_index_dict = {0: 'network', 1: 'connectType', 2: 'platform', 3: 'operator', 4: 'city', 5: 'source'}
dimension_tag_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F'}

network_index_dict = {"A0": 0, "A1": 1, "A2": 2, "A3": 3, "A4": 4}
connectType_index_dict = {"B0": 0, "B1": 1, "B2": 2, "B3": 3, "B4": 4, "B5": 5, "B6": 6, "B7": 7, "B8": 8}
platform_index_dict = {"C0": 0, "C1": 1, "C2": 2}
operator_index_dict = {"D0": 0, "D1": 1, "D2": 2, "D3": 3, "D4": 4, "D5": 5, "D6": 6, "D7": 7}
city_index_dict = {"E0": 0, "E1": 1, "E2": 2, "E3": 3, "E4": 4, "E5": 5, "E6": 6, "E7": 7, "E8": 8, "E9": 9, "E10": 10,
                   "E11": 11, "E12": 12, "E13": 13, "E14": 14, "E15": 15, "E16": 16, "E17": 17, "E18": 18, "E19": 19,
                   "E20": 20, "E21": 21, "E22": 22, "E23": 23, "E24": 24, "E25": 25, "E26": 26, "E27": 27, "E28": 28,
                   "E29": 29, "E30": 30, "E31": 31, "E32": 32, "E33": 33, "E34": 34, "E35": 35, "E36": 36, "E37": 37,
                   "E38": 38, "E39": 39, "E40": 40, "E41": 41, "E42": 42, "E43": 43, "E44": 44, "E45": 45, "E46": 46,
                   "E47": 47, "E48": 48, "E49": 49, "E50": 50, "E51": 51, "E52": 52, "E53": 53, "E54": 54, "E55": 55,
                   "E56": 56, "E57": 57, "E58": 58, "E59": 59, "E60": 60, "E61": 61, "E62": 62, "E63": 63, "E64": 64,
                   "E65": 65, "E66": 66, "E67": 67, "E68": 68, "E69": 69, "E70": 70, "E71": 71, "E72": 72, "E73": 73,
                   "E74": 74, "E75": 75, "E76": 76, "E77": 77, "E78": 78, "E79": 79, "E80": 80, "E81": 81, "E82": 82}
source_index_dict = {"F0": 0, "F1": 1, "F2": 2, "F3": 3, "F4": 4, "F5": 5, "F6": 6, "F7": 7, "F8": 8, "F9": 9,
                     "F10": 10, "F11": 11, "F12": 12, "F13": 13, "F14": 14, "F15": 15, "F16": 16, "F17": 17, "F18": 18,
                     "F19": 19, "F20": 20, "F21": 21, "F22": 22, "F23": 23, "F24": 24, "F25": 25, "F26": 26, "F27": 27,
                     "F28": 28, "F29": 29, "F30": 30, "F31": 31, "F32": 32, "F33": 33, "F34": 34, "F35": 35, "F36": 36,
                     "F37": 37, "F38": 38, "F39": 39, "F40": 40, "F41": 41, "F42": 42, "F43": 43, "F44": 44, "F45": 45,
                     "F46": 46, "F47": 47, "F48": 48, "F49": 49, "F50": 50, "F51": 51, "F52": 52, "F53": 53, "F54": 54,
                     "F55": 55, "F56": 56, "F57": 57, "F58": 58, "F59": 59, "F60": 60, "F61": 61, "F62": 62, "F63": 63,
                     "F64": 64, "F65": 65, "F66": 66, "F67": 67, "F68": 68, "F69": 69, "F70": 70, "F71": 71, "F72": 72,
                     "F73": 73, "F74": 74, "F75": 75, "F76": 76, "F77": 77, "F78": 78, "F79": 79, "F80": 80, "F81": 81,
                     "F82": 82, "F83": 83, "F84": 84, "F85": 85, "F86": 86, "F87": 87, "F88": 88, "F89": 89, "F90": 90,
                     "F91": 91, "F92": 92, "F93": 93, "F94": 94, "F95": 95, "F96": 96, "F97": 97, "F98": 98, "F99": 99,
                     "F100": 100, "F101": 101, "F102": 102, "F103": 103, "F104": 104, "F105": 105, "F106": 106,
                     "F107": 107, "F108": 108, "F109": 109, "F110": 110, "F111": 111, "F112": 112, "F113": 113,
                     "F114": 114, "F115": 115, "F116": 116, "F117": 117, "F118": 118, "F119": 119, "F120": 120,
                     "F121": 121, "F122": 122, "F123": 123, "F124": 124, "F125": 125, "F126": 126, "F127": 127,
                     "F128": 128, "F129": 129, "F130": 130, "F131": 131, "F132": 132, "F133": 133, "F134": 134,
                     "F135": 135, "F136": 136, "F137": 137, "F138": 138, "F139": 139, "F140": 140, "F141": 141,
                     "F142": 142, "F143": 143, "F144": 144, "F145": 145, "F146": 146, "F147": 147, "F148": 148,
                     "F149": 149, "F150": 150, "F151": 151, "F152": 152, "F153": 153, "F154": 154, "F155": 155,
                     "F156": 156, "F157": 157, "F158": 158, "F159": 159, "F160": 160, "F161": 161, "F162": 162,
                     "F163": 163, "F164": 164, "F165": 165, "F166": 166, "F167": 167, "F168": 168, "F169": 169,
                     "F170": 170, "F171": 171, "F172": 172, "F173": 173, "F174": 174, "F175": 175, "F176": 176,
                     "F177": 177, "F178": 178, "F179": 179, "F180": 180, "F181": 181, "F182": 182, "F183": 183,
                     "F184": 184, "F185": 185, "F186": 186, "F187": 187, "F188": 188, "F189": 189, "F190": 190,
                     "F191": 191, "F192": 192, "F193": 193, "F194": 194, "F195": 195, "F196": 196, "F197": 197,
                     "F198": 198, "F199": 199, "F200": 200, "F201": 201, "F202": 202, "F203": 203, "F204": 204,
                     "F205": 205, "F206": 206, "F207": 207, "F208": 208, "F209": 209, "F210": 210, "F211": 211,
                     "F212": 212, "F213": 213, "F214": 214, "F215": 215, "F216": 216, "F217": 217, "F218": 218,
                     "F219": 219, "F220": 220, "F221": 221, "F222": 222, "F223": 223, "F224": 224, "F225": 225,
                     "F226": 226, "F227": 227, "F228": 228, "F229": 229, "F230": 230, "F231": 231, "F232": 232,
                     "F233": 233, "F234": 234, "F235": 235, "F236": 236, "F237": 237, "F238": 238, "F239": 239,
                     "F240": 240, "F241": 241, "F242": 242, "F243": 243, "F244": 244, "F245": 245, "F246": 246,
                     "F247": 247, "F248": 248, "F249": 249, "F250": 250, "F251": 251, "F252": 252, "F253": 253,
                     "F254": 254, "F255": 255, "F256": 256, "F257": 257, "F258": 258, "F259": 259, "F260": 260,
                     "F261": 261, "F262": 262, "F263": 263, "F264": 264, "F265": 265, "F266": 266, "F267": 267,
                     "F268": 268, "F269": 269, "F270": 270, "F271": 271, "F272": 272, "F273": 273, "F274": 274,
                     "F275": 275, "F276": 276, "F277": 277, "F278": 278, "F279": 279, "F280": 280, "F281": 281,
                     "F282": 282, "F283": 283, "F284": 284, "F285": 285, "F286": 286, "F287": 287, "F288": 288,
                     "F289": 289, "F290": 290, "F291": 291, "F292": 292, "F293": 293, "F294": 294, "F295": 295,
                     "F296": 296, "F297": 297, "F298": 298, "F299": 299, "F300": 300, "F301": 301, "F302": 302,
                     "F303": 303, "F304": 304, "F305": 305, "F306": 306, "F307": 307, "F308": 308, "F309": 309}

ndarray_dict = {'network': network_index_dict, 'connectType': connectType_index_dict,
                "platform": platform_index_dict,
                'operator': operator_index_dict, 'city': city_index_dict, "source": source_index_dict}


def read_file_ndarray(day, minute, before_array, current_array, before_counter, current_counter):
    current_path = "../ImpAPTr_module/dataset/" + str(day) + "/" + str(int(minute)) + ".txt"
    before_path = "../ImpAPTr_module/dataset/" + str(day) + "/" + str(int(minute) - 5) + ".txt"

    pre_fo = open(before_path, "r")
    cur_fo = open(current_path, "r")

    pre_lines = pre_fo.readlines()
    i = 0
    for line in pre_lines:
        if i == 0:
            i += 1
            continue
        line = line[0: len(line) - 1]
        arr = line.split(",")
        network_index = ndarray_dict.get("network").get(arr[0])
        connectType_index = ndarray_dict.get("connectType").get(arr[1])
        platform_index = ndarray_dict.get("platform").get(arr[2])
        operator_index = ndarray_dict.get("operator").get(arr[3])
        city_index = ndarray_dict.get("city").get(arr[4])
        source_index = ndarray_dict.get("source").get(arr[5])
        if source_index is None:
            continue
        if int(arr[8]) == 200:
            before_counter[1] += int(arr[7])
            before_array[network_index][connectType_index][platform_index][operator_index][city_index][source_index][1] += int(arr[7])
        else:
            before_counter[0] += int(arr[7])
            before_array[network_index][connectType_index][platform_index][operator_index][city_index][source_index][0] += int(arr[7])

    # 后一个interval
    cur_lines = cur_fo.readlines()
    i = 0
    for line in cur_lines:
        if i == 0:
            i += 1
            continue
        line = line[0: len(line) - 1]
        arr = line.split(",")
        network_index = ndarray_dict.get("network").get(arr[0])
        connectType_index = ndarray_dict.get("connectType").get(arr[1])
        platform_index = ndarray_dict.get("platform").get(arr[2])
        operator_index = ndarray_dict.get("operator").get(arr[3])
        city_index = ndarray_dict.get("city").get(arr[4])
        source_index = ndarray_dict.get("source").get(arr[5])
        if source_index is None:
            continue
        if int(arr[8]) == 200:
            current_counter[1] += int(arr[7])
            current_array[network_index][connectType_index][platform_index][operator_index][city_index][source_index][
                1] += int(arr[7])
        else:
            current_counter[0] += int(arr[7])
            current_array[network_index][connectType_index][platform_index][operator_index][city_index][source_index][
                0] += int(arr[7])


def available_root_cause_descending(all_layer_nodes, number):
    all_nodes = []
    for layer in all_layer_nodes:
        for node in layer:
            all_nodes.append(node)

    all_nodes.sort(key=lambda nod: nod.contribution_power, reverse=True)
    i = 0
    for node in all_nodes:
        i += 1
        node.rank[0] = i
    all_nodes.sort(key=lambda nod: nod.diversity_power, reverse=True)
    j = 0
    for node in all_nodes:
        j += 1
        node.rank[1] = j
    all_nodes.sort(key=lambda nod: sum(nod.rank))
    all_nodes = all_nodes[0:number]
    root_causes = []
    for node in all_nodes:
        element = node.path
        root_cause_dict = {}
        for ele in element:
            root_cause_dict[dimension_index_dict.get(ele[0])] = dimension_tag_dict.get(ele[0]) + str(ele[1])
        root_causes.append(root_cause_dict)
        print(root_cause_dict)



if __name__ == '__main__':
    # following should be set manually
    before_array = np.zeros([5, 9, 3, 8, 83, 310, 2], dtype=int, order='c')
    current_array = np.zeros([5, 9, 3, 8, 83, 310, 2], dtype=int, order='c')
    # anomaly_intervals = [10, 480]  # [day, anomaly_interval]
    dimension = 6  # the number of dimension categories
    result_number = 5  # the number of available root causes


    day = sys.argv[1]
    interval = sys.argv[2]

    before_counter = [0, 0]
    current_counter = [0, 0]
    read_file_ndarray(day, interval, before_array, current_array, before_counter,
                      current_counter)
    all_layer_nodes = ImpAPTr.ImpAPTr_main(before_array, current_array, dimension, before_counter, current_counter)
    available_root_cause_descending(all_layer_nodes, result_number)
=======
import os

import numpy as np
import sys
# sys.path.append('E:/Documents/Desktop/test1')


sys.path.append(os.path.dirname(os.getcwd()))
from ImpAPTr_module import ImpAPTr

dimension_index_dict = {0: 'network', 1: 'connectType', 2: 'platform', 3: 'operator', 4: 'city', 5: 'source'}
dimension_tag_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F'}

network_index_dict = {"A0": 0, "A1": 1, "A2": 2, "A3": 3, "A4": 4}
connectType_index_dict = {"B0": 0, "B1": 1, "B2": 2, "B3": 3, "B4": 4, "B5": 5, "B6": 6, "B7": 7, "B8": 8}
platform_index_dict = {"C0": 0, "C1": 1, "C2": 2}
operator_index_dict = {"D0": 0, "D1": 1, "D2": 2, "D3": 3, "D4": 4, "D5": 5, "D6": 6, "D7": 7}
city_index_dict = {"E0": 0, "E1": 1, "E2": 2, "E3": 3, "E4": 4, "E5": 5, "E6": 6, "E7": 7, "E8": 8, "E9": 9, "E10": 10,
                   "E11": 11, "E12": 12, "E13": 13, "E14": 14, "E15": 15, "E16": 16, "E17": 17, "E18": 18, "E19": 19,
                   "E20": 20, "E21": 21, "E22": 22, "E23": 23, "E24": 24, "E25": 25, "E26": 26, "E27": 27, "E28": 28,
                   "E29": 29, "E30": 30, "E31": 31, "E32": 32, "E33": 33, "E34": 34, "E35": 35, "E36": 36, "E37": 37,
                   "E38": 38, "E39": 39, "E40": 40, "E41": 41, "E42": 42, "E43": 43, "E44": 44, "E45": 45, "E46": 46,
                   "E47": 47, "E48": 48, "E49": 49, "E50": 50, "E51": 51, "E52": 52, "E53": 53, "E54": 54, "E55": 55,
                   "E56": 56, "E57": 57, "E58": 58, "E59": 59, "E60": 60, "E61": 61, "E62": 62, "E63": 63, "E64": 64,
                   "E65": 65, "E66": 66, "E67": 67, "E68": 68, "E69": 69, "E70": 70, "E71": 71, "E72": 72, "E73": 73,
                   "E74": 74, "E75": 75, "E76": 76, "E77": 77, "E78": 78, "E79": 79, "E80": 80, "E81": 81, "E82": 82}
source_index_dict = {"F0": 0, "F1": 1, "F2": 2, "F3": 3, "F4": 4, "F5": 5, "F6": 6, "F7": 7, "F8": 8, "F9": 9,
                     "F10": 10, "F11": 11, "F12": 12, "F13": 13, "F14": 14, "F15": 15, "F16": 16, "F17": 17, "F18": 18,
                     "F19": 19, "F20": 20, "F21": 21, "F22": 22, "F23": 23, "F24": 24, "F25": 25, "F26": 26, "F27": 27,
                     "F28": 28, "F29": 29, "F30": 30, "F31": 31, "F32": 32, "F33": 33, "F34": 34, "F35": 35, "F36": 36,
                     "F37": 37, "F38": 38, "F39": 39, "F40": 40, "F41": 41, "F42": 42, "F43": 43, "F44": 44, "F45": 45,
                     "F46": 46, "F47": 47, "F48": 48, "F49": 49, "F50": 50, "F51": 51, "F52": 52, "F53": 53, "F54": 54,
                     "F55": 55, "F56": 56, "F57": 57, "F58": 58, "F59": 59, "F60": 60, "F61": 61, "F62": 62, "F63": 63,
                     "F64": 64, "F65": 65, "F66": 66, "F67": 67, "F68": 68, "F69": 69, "F70": 70, "F71": 71, "F72": 72,
                     "F73": 73, "F74": 74, "F75": 75, "F76": 76, "F77": 77, "F78": 78, "F79": 79, "F80": 80, "F81": 81,
                     "F82": 82, "F83": 83, "F84": 84, "F85": 85, "F86": 86, "F87": 87, "F88": 88, "F89": 89, "F90": 90,
                     "F91": 91, "F92": 92, "F93": 93, "F94": 94, "F95": 95, "F96": 96, "F97": 97, "F98": 98, "F99": 99,
                     "F100": 100, "F101": 101, "F102": 102, "F103": 103, "F104": 104, "F105": 105, "F106": 106,
                     "F107": 107, "F108": 108, "F109": 109, "F110": 110, "F111": 111, "F112": 112, "F113": 113,
                     "F114": 114, "F115": 115, "F116": 116, "F117": 117, "F118": 118, "F119": 119, "F120": 120,
                     "F121": 121, "F122": 122, "F123": 123, "F124": 124, "F125": 125, "F126": 126, "F127": 127,
                     "F128": 128, "F129": 129, "F130": 130, "F131": 131, "F132": 132, "F133": 133, "F134": 134,
                     "F135": 135, "F136": 136, "F137": 137, "F138": 138, "F139": 139, "F140": 140, "F141": 141,
                     "F142": 142, "F143": 143, "F144": 144, "F145": 145, "F146": 146, "F147": 147, "F148": 148,
                     "F149": 149, "F150": 150, "F151": 151, "F152": 152, "F153": 153, "F154": 154, "F155": 155,
                     "F156": 156, "F157": 157, "F158": 158, "F159": 159, "F160": 160, "F161": 161, "F162": 162,
                     "F163": 163, "F164": 164, "F165": 165, "F166": 166, "F167": 167, "F168": 168, "F169": 169,
                     "F170": 170, "F171": 171, "F172": 172, "F173": 173, "F174": 174, "F175": 175, "F176": 176,
                     "F177": 177, "F178": 178, "F179": 179, "F180": 180, "F181": 181, "F182": 182, "F183": 183,
                     "F184": 184, "F185": 185, "F186": 186, "F187": 187, "F188": 188, "F189": 189, "F190": 190,
                     "F191": 191, "F192": 192, "F193": 193, "F194": 194, "F195": 195, "F196": 196, "F197": 197,
                     "F198": 198, "F199": 199, "F200": 200, "F201": 201, "F202": 202, "F203": 203, "F204": 204,
                     "F205": 205, "F206": 206, "F207": 207, "F208": 208, "F209": 209, "F210": 210, "F211": 211,
                     "F212": 212, "F213": 213, "F214": 214, "F215": 215, "F216": 216, "F217": 217, "F218": 218,
                     "F219": 219, "F220": 220, "F221": 221, "F222": 222, "F223": 223, "F224": 224, "F225": 225,
                     "F226": 226, "F227": 227, "F228": 228, "F229": 229, "F230": 230, "F231": 231, "F232": 232,
                     "F233": 233, "F234": 234, "F235": 235, "F236": 236, "F237": 237, "F238": 238, "F239": 239,
                     "F240": 240, "F241": 241, "F242": 242, "F243": 243, "F244": 244, "F245": 245, "F246": 246,
                     "F247": 247, "F248": 248, "F249": 249, "F250": 250, "F251": 251, "F252": 252, "F253": 253,
                     "F254": 254, "F255": 255, "F256": 256, "F257": 257, "F258": 258, "F259": 259, "F260": 260,
                     "F261": 261, "F262": 262, "F263": 263, "F264": 264, "F265": 265, "F266": 266, "F267": 267,
                     "F268": 268, "F269": 269, "F270": 270, "F271": 271, "F272": 272, "F273": 273, "F274": 274,
                     "F275": 275, "F276": 276, "F277": 277, "F278": 278, "F279": 279, "F280": 280, "F281": 281,
                     "F282": 282, "F283": 283, "F284": 284, "F285": 285, "F286": 286, "F287": 287, "F288": 288,
                     "F289": 289, "F290": 290, "F291": 291, "F292": 292, "F293": 293, "F294": 294, "F295": 295,
                     "F296": 296, "F297": 297, "F298": 298, "F299": 299, "F300": 300, "F301": 301, "F302": 302,
                     "F303": 303, "F304": 304, "F305": 305, "F306": 306, "F307": 307, "F308": 308, "F309": 309}

ndarray_dict = {'network': network_index_dict, 'connectType': connectType_index_dict,
                "platform": platform_index_dict,
                'operator': operator_index_dict, 'city': city_index_dict, "source": source_index_dict}


def read_file_ndarray(day, minute, before_array, current_array, before_counter, current_counter):
    current_path = "../ImpAPTr_module/dataset/" + str(day) + "/" + str(int(minute)) + ".txt"
    before_path = "../ImpAPTr_module/dataset/" + str(day) + "/" + str(int(minute) - 5) + ".txt"

    pre_fo = open(before_path, "r")
    cur_fo = open(current_path, "r")

    pre_lines = pre_fo.readlines()
    i = 0
    for line in pre_lines:
        if i == 0:
            i += 1
            continue
        line = line[0: len(line) - 1]
        arr = line.split(",")
        network_index = ndarray_dict.get("network").get(arr[0])
        connectType_index = ndarray_dict.get("connectType").get(arr[1])
        platform_index = ndarray_dict.get("platform").get(arr[2])
        operator_index = ndarray_dict.get("operator").get(arr[3])
        city_index = ndarray_dict.get("city").get(arr[4])
        source_index = ndarray_dict.get("source").get(arr[5])
        if source_index is None:
            continue
        if int(arr[8]) == 200:
            before_counter[1] += int(arr[7])
            before_array[network_index][connectType_index][platform_index][operator_index][city_index][source_index][1] += int(arr[7])
        else:
            before_counter[0] += int(arr[7])
            before_array[network_index][connectType_index][platform_index][operator_index][city_index][source_index][0] += int(arr[7])

    # 后一个interval
    cur_lines = cur_fo.readlines()
    i = 0
    for line in cur_lines:
        if i == 0:
            i += 1
            continue
        line = line[0: len(line) - 1]
        arr = line.split(",")
        network_index = ndarray_dict.get("network").get(arr[0])
        connectType_index = ndarray_dict.get("connectType").get(arr[1])
        platform_index = ndarray_dict.get("platform").get(arr[2])
        operator_index = ndarray_dict.get("operator").get(arr[3])
        city_index = ndarray_dict.get("city").get(arr[4])
        source_index = ndarray_dict.get("source").get(arr[5])
        if source_index is None:
            continue
        if int(arr[8]) == 200:
            current_counter[1] += int(arr[7])
            current_array[network_index][connectType_index][platform_index][operator_index][city_index][source_index][
                1] += int(arr[7])
        else:
            current_counter[0] += int(arr[7])
            current_array[network_index][connectType_index][platform_index][operator_index][city_index][source_index][
                0] += int(arr[7])


def available_root_cause_descending(all_layer_nodes, number):
    all_nodes = []
    for layer in all_layer_nodes:
        for node in layer:
            all_nodes.append(node)

    all_nodes.sort(key=lambda nod: nod.contribution_power, reverse=True)
    i = 0
    for node in all_nodes:
        i += 1
        node.rank[0] = i
    all_nodes.sort(key=lambda nod: nod.diversity_power, reverse=True)
    j = 0
    for node in all_nodes:
        j += 1
        node.rank[1] = j
    all_nodes.sort(key=lambda nod: sum(nod.rank))
    all_nodes = all_nodes[0:number]
    root_causes = []
    for node in all_nodes:
        element = node.path
        root_cause_dict = {}
        for ele in element:
            root_cause_dict[dimension_index_dict.get(ele[0])] = dimension_tag_dict.get(ele[0]) + str(ele[1])
        root_causes.append(root_cause_dict)
        print(root_cause_dict)



if __name__ == '__main__':
    # following should be set manually
    before_array = np.zeros([5, 9, 3, 8, 83, 310, 2], dtype=int, order='c')
    current_array = np.zeros([5, 9, 3, 8, 83, 310, 2], dtype=int, order='c')
    # anomaly_intervals = [10, 480]  # [day, anomaly_interval]
    dimension = 6  # the number of dimension categories
    result_number = 5  # the number of available root causes


    day = sys.argv[1]
    interval = sys.argv[2]

    before_counter = [0, 0]
    current_counter = [0, 0]
    read_file_ndarray(day, interval, before_array, current_array, before_counter,
                      current_counter)
    all_layer_nodes = ImpAPTr.ImpAPTr_main(before_array, current_array, dimension, before_counter, current_counter)
    available_root_cause_descending(all_layer_nodes, result_number)
>>>>>>> 59b5fb7231d56e643921b16307d067d95b2c5b41
