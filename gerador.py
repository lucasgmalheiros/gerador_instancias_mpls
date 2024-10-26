import numpy as np

def uniform(seed, low, high):
    """Generator that uses the linear congruential method"""
    m = 2147483647
    a = 16807
    b = 127773
    c = 2836

    k = seed // b
    seed = a * (seed % b) - k * c
    if seed < 0:
        seed += m
    value_0_1 = seed / m
    uniform_ret = low + value_0_1 * (high - low)
    return uniform_ret, seed


def generate_data(name, n_products, n_plants, n_periods, type1, type2, type3, n_instances=10):
    """Main function for reading parameters and constructing .dat files"""
    # Read parameters from 'gdata.dat'
    input_filename = 'gdata.dat'
    try:
        with open(input_filename, 'r') as file:
            lines = file.readlines()
    except IOError:
        print('Error opening the data file!!!')

    # Initialize parameters
    params = {}
    # Process each line to extract parameters
    for line in lines:
        line = line.strip()
        if not line or '=' not in line:
            continue  # Skip empty lines and lines without '='
        tokens = line.split('=')
        key = tokens[0].strip()
        value = float(tokens[1].strip())
        params[key] = value

    # Assign parameters
    MIN_SETUP_COST = params.get('min_setup_cost', 0)
    MAX_SETUP_COST = params.get('max_setup_cost', 0)
    MIN_PRODUCTION_COST = params.get('min_production_cost', 0)
    MAX_PRODUCTION_COST = params.get('max_production_cost', 0)
    MIN_INVENTORY_COST = params.get('min_inventory_cost', 0)
    MAX_INVENTORY_COST = params.get('max_inventory_cost', 0)
    MIN_DEMAND = params.get('min_demand', 0)
    MAX_DEMAND = params.get('max_demand', 0)
    MIN_PRODUCTION_TIME = params.get('min_production_time', 0)
    MAX_PRODUCTION_TIME = params.get('max_production_time', 0)
    MIN_SETUP_TIME = params.get('min_setup_time', 0)
    MAX_SETUP_TIME = params.get('max_setup_time', 0)
    MIN_TRANSPORT_COST = params.get('min_transport_cost', 0)
    MAX_TRANSPORT_COST = params.get('max_transport_cost', 0)

    # If any parameter is missing, print an error
    required_params = [
        'min_setup_cost', 'max_setup_cost', 
        'min_production_cost', 'max_production_cost',
        'min_inventory_cost', 'max_inventory_cost', 
        'min_demand', 'max_demand',
        'min_production_time', 'max_production_time', 
        'min_setup_time', 'max_setup_time',
        'min_transport_cost', 'max_transport_cost'
        ]
    for param in required_params:
        if param not in params:
            print(f'Missing parameter "{param}" in gdata.dat')

    # Open 'seed.dat' and read seeds
    try:
        with open('seed.dat', 'r') as file:
            seed_lines = file.readlines()
    except IOError:
        print('Error opening the data file!!!')

    for instance_num in range(n_instances):  # Controls the number of instances generated from 1 to 10 (limited by number of seeds)
        # Read seed
        tokens = seed_lines[instance_num].split('=')
        seed = int(tokens[-1].strip())

        output_filename = f'{name}{instance_num}_{n_periods}_{n_plants}_{n_products}.dat'

        try:
            dat = open(output_filename, 'w')
        except IOError:
            print('Error opening the output file!!!')

        # Generate data
        # Initialize arrays with numpy
        inventory_costs = np.zeros(n_products)  # Inventory costs for each product
        production_costs = np.zeros((n_plants, n_products))  # Production costs by plant and product
        setup_costs = np.zeros((n_plants, n_products))  # Setup costs by plant and product
        production_times = np.zeros((n_plants, n_products))  # Production time by plant and product
        setup_times = np.zeros((n_plants, n_products))  # Setup time by plant and product
        demands = np.zeros((n_periods, n_products))  # Demand by period and product
        transport_costs = np.zeros((n_plants, n_plants))  # Transport costs from plant to plant
        capacities = np.zeros(n_plants)  # Capacity per plant

        # Costs data
        for i in range(n_products):
            inventory_costs[i], seed = uniform(seed, MIN_INVENTORY_COST, MAX_INVENTORY_COST)
            for j in range(n_plants):
                production_costs[j, i], seed = uniform(seed, MIN_PRODUCTION_COST, MAX_PRODUCTION_COST)
                setup_costs[j, i], seed = uniform(seed, MIN_SETUP_COST, MAX_SETUP_COST)

        # Times data
        for i in range(n_products):
            for j in range(n_plants):
                production_times[j, i], seed = uniform(seed, MIN_PRODUCTION_TIME, MAX_PRODUCTION_TIME)
                setup_times[j, i], seed = uniform(seed, MIN_SETUP_TIME, MAX_SETUP_TIME)

        # Demand matrix
        for i in range(n_products):
            for t in range(n_periods):
                value, seed = uniform(seed, MIN_DEMAND, MAX_DEMAND)
                demands[t, i] = 1.0 * int(value)

        # Symmetric transport costs matrix
        for j in range(n_plants):
            # Lower triangular matrix
            for k in range(j):
                if j == k:  # Main diagonal
                    transport_costs[j, k] = 0
                else:
                    transport_costs[j, k], seed = uniform(seed, MIN_TRANSPORT_COST, MAX_TRANSPORT_COST)
                # Enforce symmetry over upper triangular matrix
                transport_costs[k, j] = transport_costs[j, k]

        # Calculate capacity for each plant
        for j in range(n_plants):
            sum_necessities = 0
            for i in range(n_products):
                for t in range(n_periods):
                    sum_necessities += setup_times[j, i] + production_times[j, i] * demands[t, i]
            capacities[j] = np.ceil((sum_necessities / n_periods) * type3)  # Capacidade ajustada pelo tipo3


        # OUTPUT FILE FORMATTING
        # Number of products | Number of periods
        print(f'{n_products} {n_periods}', file=dat)
        # Number of machines
        print(f'{n_plants}', file=dat)
        # Capacities calculated above
        for j in range(n_plants):
            print(f'{capacities[j]:10.0f}', file=dat)

        # Production time | Setup time | Setup cost | Production cost
        for j in range(n_plants):
            for i in range(n_products):
                print(f'{production_times[j, i]:5.1f} {setup_times[j, i]:5.1f} {setup_costs[j, i]:5.1f} {production_costs[j, i]:5.1f}', file=dat)

        # Inventory costs line
        for i in range(n_products):
            print(f'{inventory_costs[i]:5.1f} ', end='', file=dat)
        print('', file=dat)
        
        # Demand matrix (one period per line)
        for t in range(n_periods):
            for i in range(n_products):
                print(f'{int(demands[t, i]):5d} ', end='', file=dat)
            print('', file=dat)

        # Transport costs matrix
        for j in range(n_plants):
            for k in range(n_plants):
                print(f'{transport_costs[j, k]:5.2f} ', end='', file=dat)
            print('', file=dat)

        dat.close()


def run_problems(type_, start, end, name, setup_cost, setup_time, cap_type):
    """Defines the number of products (NN), periods (t) and machines (MM) and calls the generate_data function"""
    # vectorN = [12]
    # for t in range(6, 7):
    #     for MM in range(2, 3):
    #         for id in range(0, 1):
    #             NN = vectorN[id]
    #             generate_data(name, NN, MM, t)
    generate_data(name, 6, 6, 12, type1=setup_cost, type2=setup_time, type3=cap_type, n_instances=1,)


def main():
    run_problems('CASATA', 0, 9, 'AAA0', 1.5, 10.0, 0.9)
    # run_problems('CASATB', 0, 9, 'AAB0', 1.0, 10.0, 0.9)
    # run_problems('CASBTA', 0, 9, 'ABA0', 1.5, 1.0, 0.9)
    # run_problems('CASBTB', 0, 9, 'ABB0', 1.0, 1.0, 0.9)
    # run_problems('CNSATA', 0, 9, 'NAA0', 1.5, 10.0, 1.0)
    # run_problems('CNSATB', 0, 9, 'NAB0', 1.0, 10.0, 1.0)
    # run_problems('CNSBTA', 0, 9, 'NBA0', 1.5, 1.0, 1.0)
    # run_problems('CNSBTB', 0, 9, 'NBB0', 1.0, 1.0, 1.0)


if __name__ == '__main__':
    main()
