import numpy as np

def uniform(seed: int, low: float, high: float) -> tuple:
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


def generate_data(name: str, n_periods: int, n_plants: int, n_products: int, type1: float, type2: float, type3: float, n_instances: int=10) -> None:
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

        # Generate data
        # Initialize arrays with numpy
        inventory_costs = np.zeros(n_products * n_plants)  # Inventory costs for each product
        production_costs = np.zeros((n_plants, n_products))  # Production costs by plant and product
        setup_costs = np.zeros((n_plants, n_products))  # Setup costs by plant and product
        production_times = np.zeros((n_plants, n_products))  # Production time by plant and product
        setup_times = np.zeros((n_plants, n_products))  # Setup time by plant and product
        demands = np.zeros((n_periods, n_products * n_plants))  # Demand by period and product
        transport_costs = np.zeros((n_plants, n_plants))  # Transport costs from plant to plant
        capacities = np.zeros(n_plants)  # Capacity per plant
        
        # Inventory costs data
        for z in range(n_products * n_plants):
            inventory_costs[z], seed = uniform(seed, MIN_INVENTORY_COST, MAX_INVENTORY_COST)

        # Production and setup costs data
        for i in range(n_products):
            for j in range(n_plants):
                production_costs[j, i], seed = uniform(seed, MIN_PRODUCTION_COST, MAX_PRODUCTION_COST)
                setup_costs[j, i], seed = uniform(seed, MIN_SETUP_COST, MAX_SETUP_COST)
                # Apply type 2 for setup costs
                setup_costs[j, i] *= type2

        # Times data
        for i in range(n_products):
            for j in range(n_plants):
                production_times[j, i], seed = uniform(seed, MIN_PRODUCTION_TIME, MAX_PRODUCTION_TIME)
                setup_times[j, i], seed = uniform(seed, MIN_SETUP_TIME, MAX_SETUP_TIME)
                # Apply type 1 for setup times
                setup_times[j, i] *= type1

        # Demand matrix
        for t in range(n_periods):
            for z in range(n_products * n_plants):
                value, seed = uniform(seed, MIN_DEMAND, MAX_DEMAND)
                demands[t, z] = np.ceil(value)

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
            capacities[j] = np.ceil(sum_necessities / n_periods)
            # Apply type 3 for capacities values
            capacities[j] *= type3


        # OUTPUT FILE FORMATTING
        output_filename = f'multi_plant_instances/{name}{instance_num}_{n_periods}_{n_plants}_{n_products}.dat'
        try:
            dat = open(output_filename, 'w')
        except IOError:
            print('Error opening the output file!!!')

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
        for z in range(n_products * n_plants):
            print(f'{inventory_costs[z]:5.1f} ', end='', file=dat)
        print('', file=dat)

        # Demand matrix (one period per line)
        for t in range(n_periods):
            for z in range(n_products * n_plants):
                print(f'{int(demands[t, z]):5d} ', end='', file=dat)
            print('', file=dat)

        # Transport costs matrix
        for j in range(n_plants):
            for k in range(n_plants):
                print(f'{transport_costs[j, k]:5.2f} ', end='', file=dat)
            print('', file=dat)

        dat.close()


def run_problems(type_: str, start: int, end: int, name: str, setup_time: float, setup_cost: float, cap_type:float) -> None:
    """Defines the number of products, periods and machines, and calls the generate_data function"""
    for t in [12]:  # Periods
        for j in [2, 4, 6, 15, 20]:  # Plants
            for i in [10, 30, 60, 90, 120]:  # Products
                generate_data(name, n_periods=t, n_plants=j, n_products=i, type1=setup_time, type2=setup_cost, type3=cap_type)


def main() -> None:
    run_problems('CASATA', 0, 9, 'AAA0', 1.5, 10.0, 0.9)
    run_problems('CASATB', 0, 9, 'AAB0', 1.0, 10.0, 0.9)
    run_problems('CASBTA', 0, 9, 'ABA0', 1.5, 1.0, 0.9)
    run_problems('CASBTB', 0, 9, 'ABB0', 1.0, 1.0, 0.9)
    run_problems('CNSATA', 0, 9, 'NAA0', 1.5, 10.0, 1.0)
    run_problems('CNSATB', 0, 9, 'NAB0', 1.0, 10.0, 1.0)
    run_problems('CNSBTA', 0, 9, 'NBA0', 1.5, 1.0, 1.0)
    run_problems('CNSBTB', 0, 9, 'NBB0', 1.0, 1.0, 1.0)


if __name__ == '__main__':
    main()
