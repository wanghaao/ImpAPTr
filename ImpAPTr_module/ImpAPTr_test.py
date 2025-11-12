"""
ImpAPTr Test Script

This script provides a testing framework for the ImpAPTr algorithm.
It reads service call data from files, runs the ImpAPTr analysis, and outputs
the top anomaly clues ranked by contribution power and diversity power.

Usage:
    python ImpAPTr_test.py [day] [interval]

    Example:
        python ImpAPTr_test.py 10 480    # Analyze March 10, interval 480 (08:00-08:05)
        python ImpAPTr_test.py 19 680    # Analyze March 19, interval 680 (11:20-11:25)

Author: Hao Wang
Date: 2020
"""

import os
import numpy as np
import sys

# Add parent directory to path to import ImpAPTr module
sys.path.append(os.path.dirname(os.getcwd()))
from ImpAPTr_module import ImpAPTr


# =============================================================================
# Dimension and Index Dictionaries
# =============================================================================
# These dictionaries map between dimension names, indices, and value encodings

# Map dimension index to human-readable name
dimension_index_dict = {
    0: 'network',      # Network type
    1: 'connectType',  # Connection type
    2: 'platform',     # Platform (e.g., iOS, Android, Web)
    3: 'operator',     # Network operator/ISP
    4: 'city',         # City location
    5: 'source'        # Request source
}

# Map dimension index to letter tag (for encoding attribute values)
dimension_tag_dict = {
    0: 'A',  # Network -> A0, A1, A2, ...
    1: 'B',  # ConnectType -> B0, B1, B2, ...
    2: 'C',  # Platform -> C0, C1, C2, ...
    3: 'D',  # Operator -> D0, D1, D2, ...
    4: 'E',  # City -> E0, E1, E2, ...
    5: 'F'   # Source -> F0, F1, F2, ...
}

# Map encoded values to array indices for each dimension
# Network dimension: 5 values (A0-A4)
network_index_dict = {
    "A0": 0, "A1": 1, "A2": 2, "A3": 3, "A4": 4
}

# Connection type dimension: 9 values (B0-B8)
connectType_index_dict = {
    "B0": 0, "B1": 1, "B2": 2, "B3": 3, "B4": 4,
    "B5": 5, "B6": 6, "B7": 7, "B8": 8
}

# Platform dimension: 3 values (C0-C2)
platform_index_dict = {
    "C0": 0, "C1": 1, "C2": 2
}

# Operator dimension: 8 values (D0-D7)
operator_index_dict = {
    "D0": 0, "D1": 1, "D2": 2, "D3": 3,
    "D4": 4, "D5": 5, "D6": 6, "D7": 7
}

# City dimension: 83 values (E0-E82)
city_index_dict = {
    "E0": 0, "E1": 1, "E2": 2, "E3": 3, "E4": 4, "E5": 5, "E6": 6, "E7": 7, "E8": 8, "E9": 9,
    "E10": 10, "E11": 11, "E12": 12, "E13": 13, "E14": 14, "E15": 15, "E16": 16, "E17": 17, "E18": 18, "E19": 19,
    "E20": 20, "E21": 21, "E22": 22, "E23": 23, "E24": 24, "E25": 25, "E26": 26, "E27": 27, "E28": 28, "E29": 29,
    "E30": 30, "E31": 31, "E32": 32, "E33": 33, "E34": 34, "E35": 35, "E36": 36, "E37": 37, "E38": 38, "E39": 39,
    "E40": 40, "E41": 41, "E42": 42, "E43": 43, "E44": 44, "E45": 45, "E46": 46, "E47": 47, "E48": 48, "E49": 49,
    "E50": 50, "E51": 51, "E52": 52, "E53": 53, "E54": 54, "E55": 55, "E56": 56, "E57": 57, "E58": 58, "E59": 59,
    "E60": 60, "E61": 61, "E62": 62, "E63": 63, "E64": 64, "E65": 65, "E66": 66, "E67": 67, "E68": 68, "E69": 69,
    "E70": 70, "E71": 71, "E72": 72, "E73": 73, "E74": 74, "E75": 75, "E76": 76, "E77": 77, "E78": 78, "E79": 79,
    "E80": 80, "E81": 81, "E82": 82
}

# Source dimension: 310 values (F0-F309)
source_index_dict = {f"F{i}": i for i in range(310)}

# Combined dictionary for easy lookup
ndarray_dict = {
    'network': network_index_dict,
    'connectType': connectType_index_dict,
    'platform': platform_index_dict,
    'operator': operator_index_dict,
    'city': city_index_dict,
    'source': source_index_dict
}


# =============================================================================
# Data Loading Functions
# =============================================================================

def read_file_ndarray(day, minute, before_array, current_array, before_counter, current_counter):
    """
    Read service call data from files for the current and previous time intervals.

    This function loads data from text files containing service call records,
    parses each record, and populates multi-dimensional arrays with request counts.

    Data file format (one record per line):
        A4,B0,C1,D1,E30,F9,6055,2,200
        Where:
        - A4-F9: Dimensional attribute values (network, connectType, platform, operator, city, source)
        - 6055: (Unused in this code)
        - 2: Number of requests
        - 200: HTTP status code (200=success, others=failure)

    Args:
        day (str): Day of the month
        minute (str): Time interval index (e.g., 480 = 08:00-08:05)
        before_array (ndarray): Array to populate with previous interval data [5,9,3,8,83,310,2]
        current_array (ndarray): Array to populate with current interval data [5,9,3,8,83,310,2]
        before_counter (list): [failure_count, success_count] for previous interval (modified in place)
        current_counter (list): [failure_count, success_count] for current interval (modified in place)

    Returns:
        None (arrays and counters are modified in place)

    Note:
        The last dimension of arrays has size 2: [0]=failures, [1]=successes
    """
    # Construct file paths for current and previous (5 minutes earlier) intervals
    current_path = "../ImpAPTr_module/dataset/" + str(day) + "/" + str(int(minute)) + ".txt"
    before_path = "../ImpAPTr_module/dataset/" + str(day) + "/" + str(int(minute) - 5) + ".txt"

    # Read previous interval data
    pre_fo = open(before_path, "r")
    cur_fo = open(current_path, "r")

    pre_lines = pre_fo.readlines()
    i = 0
    for line in pre_lines:
        # Skip header line
        if i == 0:
            i += 1
            continue

        # Parse line
        line = line.strip()  # Remove trailing newline
        arr = line.split(",")

        # Map encoded values to array indices
        network_index = ndarray_dict.get("network").get(arr[0])
        connectType_index = ndarray_dict.get("connectType").get(arr[1])
        platform_index = ndarray_dict.get("platform").get(arr[2])
        operator_index = ndarray_dict.get("operator").get(arr[3])
        city_index = ndarray_dict.get("city").get(arr[4])
        source_index = ndarray_dict.get("source").get(arr[5])

        # Skip if source is not in dictionary (data quality issue)
        if source_index is None:
            continue

        # Count successes and failures
        request_count = int(arr[7])
        status_code = int(arr[8])

        if status_code == 200:  # Success
            before_counter[1] += request_count
            before_array[network_index][connectType_index][platform_index][operator_index][city_index][source_index][1] += request_count
        else:  # Failure
            before_counter[0] += request_count
            before_array[network_index][connectType_index][platform_index][operator_index][city_index][source_index][0] += request_count

    # Read current interval data (same process as above)
    cur_lines = cur_fo.readlines()
    i = 0
    for line in cur_lines:
        if i == 0:
            i += 1
            continue

        line = line.strip()
        arr = line.split(",")

        network_index = ndarray_dict.get("network").get(arr[0])
        connectType_index = ndarray_dict.get("connectType").get(arr[1])
        platform_index = ndarray_dict.get("platform").get(arr[2])
        operator_index = ndarray_dict.get("operator").get(arr[3])
        city_index = ndarray_dict.get("city").get(arr[4])
        source_index = ndarray_dict.get("source").get(arr[5])

        if source_index is None:
            continue

        request_count = int(arr[7])
        status_code = int(arr[8])

        if status_code == 200:  # Success
            current_counter[1] += request_count
            current_array[network_index][connectType_index][platform_index][operator_index][city_index][source_index][1] += request_count
        else:  # Failure
            current_counter[0] += request_count
            current_array[network_index][connectType_index][platform_index][operator_index][city_index][source_index][0] += request_count

    # Close file handles
    pre_fo.close()
    cur_fo.close()


# =============================================================================
# Result Processing Functions
# =============================================================================

def available_root_cause_descending(all_layer_nodes, number):
    """
    Rank and display the top anomaly clues from ImpAPTr analysis results.

    This function takes the candidate nodes from all layers, ranks them using
    a combination of contribution power and diversity power, and outputs the
    top N clues that are most likely to be root causes of the anomaly.

    Ranking algorithm:
    1. Rank all nodes by contribution_power (descending) -> rank[0]
    2. Rank all nodes by diversity_power (descending) -> rank[1]
    3. Sort by sum of ranks (ascending) to get final ranking

    Args:
        all_layer_nodes (list): List of lists, where each inner list contains
                               Node objects from one layer of the pruning tree
        number (int): Number of top anomaly clues to display

    Returns:
        None (results are printed to console)

    Output format:
        Each line shows one anomaly clue as a dictionary, e.g.:
        {'network': 'A4', 'city': 'E30', 'source': 'F9'}
        This indicates that the combination of Network=A4, City=E30, Source=F9
        is a likely clue to the anomaly.
    """
    # Collect all nodes from all layers into a single list
    all_nodes = []
    for layer in all_layer_nodes:
        for node in layer:
            all_nodes.append(node)

    # Rank by contribution power (higher is better)
    all_nodes.sort(key=lambda nod: nod.contribution_power, reverse=True)
    i = 0
    for node in all_nodes:
        i += 1
        node.rank[0] = i

    # Rank by diversity power (higher is better)
    all_nodes.sort(key=lambda nod: nod.diversity_power, reverse=True)
    j = 0
    for node in all_nodes:
        j += 1
        node.rank[1] = j

    # Final ranking by sum of ranks (lower sum is better)
    all_nodes.sort(key=lambda nod: sum(nod.rank))

    # Select top N nodes
    all_nodes = all_nodes[0:number]

    # Convert node paths to human-readable format and print
    root_causes = []
    print("\n" + "="*60)
    print("Top {} Anomaly Clues:".format(number))
    print("="*60)

    for idx, node in enumerate(all_nodes, 1):
        element = node.path
        root_cause_dict = {}

        # Convert path to dictionary of dimension:value pairs
        for ele in element:
            dimension_name = dimension_index_dict.get(ele[0])
            dimension_value = dimension_tag_dict.get(ele[0]) + str(ele[1])
            root_cause_dict[dimension_name] = dimension_value

        root_causes.append(root_cause_dict)

        # Print with additional metrics
        print(f"\n{idx}. {root_cause_dict}")
        print(f"   Contribution Power: {node.contribution_power:.6f}")
        print(f"   Diversity Power: {node.diversity_power:.6f}")
        print(f"   Impact Factor: {node.impact_factor:.6f}")
        print(f"   Requests: {node.request_number[1]} (current), {node.request_number[0]} (previous)")
        print(f"   Failures: {node.fail_number[1]} (current), {node.fail_number[0]} (previous)")

    print("\n" + "="*60)


# =============================================================================
# Main Execution
# =============================================================================

if __name__ == '__main__':
    """
    Main execution block for running ImpAPTr analysis.
    
    Command line arguments:
        sys.argv[1]: day - Day of the month (e.g., 10 for March 10)
        sys.argv[2]: interval - Time interval index (e.g., 480 for 08:00-08:05)
        
    The script:
    1. Initializes multi-dimensional arrays for data storage
    2. Reads service call data from files
    3. Runs ImpAPTr algorithm to identify anomaly clues
    4. Displays top-ranked anomaly clues
    """

    # Initialize multi-dimensional arrays
    # Dimensions: [network(5), connectType(9), platform(3), operator(8), city(83), source(310), status(2)]
    # Last dimension: [0]=failures, [1]=successes
    before_array = np.zeros([5, 9, 3, 8, 83, 310, 2], dtype=int, order='c')
    current_array = np.zeros([5, 9, 3, 8, 83, 310, 2], dtype=int, order='c')

    # Configuration parameters
    dimension = 6  # Number of dimensional attributes (network, connectType, platform, operator, city, source)
    result_number = 5  # Number of top anomaly clues to display

    # Parse command line arguments
    if len(sys.argv) < 3:
        print("Usage: python ImpAPTr_test.py [day] [interval]")
        print("Example: python ImpAPTr_test.py 10 480")
        sys.exit(1)

    day = sys.argv[1]
    interval = sys.argv[2]

    print("\n" + "="*60)
    print(f"ImpAPTr Anomaly Analysis")
    print("="*60)
    print(f"Date: March {day}, 2020")
    print(f"Time Interval: {interval} (comparing with {int(interval)-5})")
    print("="*60)

    # Initialize counters for total successes and failures
    # Format: [failures, successes]
    before_counter = [0, 0]
    current_counter = [0, 0]

    # Read data from files
    print("\nLoading data...")
    read_file_ndarray(day, interval, before_array, current_array, before_counter, current_counter)

    # Display data statistics
    print(f"\nPrevious Interval (ID: {int(interval)-5}):")
    print(f"  Total Requests: {sum(before_counter)}")
    print(f"  Successes: {before_counter[1]} ({100*before_counter[1]/sum(before_counter):.2f}%)")
    print(f"  Failures: {before_counter[0]} ({100*before_counter[0]/sum(before_counter):.2f}%)")

    print(f"\nCurrent Interval (ID: {interval}):")
    print(f"  Total Requests: {sum(current_counter)}")
    print(f"  Successes: {current_counter[1]} ({100*current_counter[1]/sum(current_counter):.2f}%)")
    print(f"  Failures: {current_counter[0]} ({100*current_counter[0]/sum(current_counter):.2f}%)")

    # Calculate success rate decline
    prev_success_rate = before_counter[1] / sum(before_counter) if sum(before_counter) > 0 else 0
    curr_success_rate = current_counter[1] / sum(current_counter) if sum(current_counter) > 0 else 0
    decline = prev_success_rate - curr_success_rate

    print(f"\nSuccess Rate Change: {decline*100:.3f}% decline")
    print("="*60)

    # Run ImpAPTr algorithm
    print("\nRunning ImpAPTr analysis...")
    all_layer_nodes = ImpAPTr.ImpAPTr_main(before_array, current_array, dimension, before_counter, current_counter)

    # Display results
    available_root_cause_descending(all_layer_nodes, result_number)

