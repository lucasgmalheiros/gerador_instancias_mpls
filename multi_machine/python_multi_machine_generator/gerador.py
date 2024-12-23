def unif(seed, low, high):
    """Gerador que utiliza método da congruência linear"""
    m = 2147483647
    a = 16807
    b = 127773
    c = 2836

    k = seed // b
    seed = a * (seed % b) - k * c
    if seed < 0:
        seed += m
    value_0_1 = seed / m
    unif_ret = low + value_0_1 * (high - low)
    return unif_ret, seed


def Gera_dados(nome, NN, MM, TT):
    """Função principal de leitura dos parâmetros e contrução dos arquivos .dat"""
    # Read parameters from "gdado.dat"
    fname_ent = "../gdado.dat"
    try:
        with open(fname_ent, "r") as arq:
            lines = arq.readlines()
    except IOError:
        print("Erro na abertura do arquivo de dados !!!")
        return 1

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
    L_min_s = params.get('mincustosetup', 0)
    L_max_s = params.get('maxcustosetup', 0)
    L_min_c = params.get('mincustoprod', 0)
    L_max_c = params.get('maxcustoprod', 0)
    L_min_h = params.get('mincustoestoq', 0)
    L_max_h = params.get('maxcustoestoq', 0)
    L_min_d = params.get('mindemanda', 0)
    L_max_d = params.get('maxdemanda', 0)
    L_min_b = params.get('mintempoprod', 0)
    L_max_b = params.get('maxtempoprod', 0)
    L_min_f = params.get('mintemposetup', 0)
    L_max_f = params.get('maxtemposetup', 0)
    # If any parameter is missing, print an error
    required_params = ['mintemposetup', 'maxtemposetup', 'mincustoprod', 'maxcustoprod',
                       'mincustoestoq', 'maxcustoestoq', 'mindemanda', 'maxdemanda',
                       'mintempoprod', 'maxtempoprod', 'mincustosetup', 'maxcustosetup']
    for param in required_params:
        if param not in params:
            print(f"Missing parameter '{param}' in gdado.dat")
            return 1

    # Open "semente.dat" and read seeds
    try:
        with open("../semente.dat", "r") as arq:
            seed_lines = arq.readlines()
    except IOError:
        print("Erro na abertura do arquivo de dados !!!")
        return 1

    for narq in range(10):
        # Read seed
        tokens = seed_lines[narq].split('=')
        seed = int(tokens[-1].strip())

        fname_dat = f"{nome}{narq}_{NN}_{MM}_{TT}.dat"

        try:
            dat = open(fname_dat, "w")
        except IOError:
            print("Erro na abertura do arquivo de dados !!!")
            return 1

        # Generate data
        NN_index = NN  # To match C's 1-based indexing
        MM_index = MM
        TT_index = TT

        hpdc = [0.0] * NN
        cpdc = [ [0.0]*NN for _ in range(MM)]
        spdc = [ [0.0]*NN for _ in range(MM)]
        bpdc = [ [0.0]*NN for _ in range(MM)]
        fpdc = [ [0.0]*NN for _ in range(MM)]
        dpdc = [ [0.0]*NN for _ in range(TT)]

        for ii in range(NN):
            hpdc[ii], seed = unif(seed, L_min_h, L_max_h)
            for jj in range(MM):
                cpdc[jj][ii], seed = unif(seed, L_min_c, L_max_c)
                spdc[jj][ii], seed = unif(seed, L_min_s, L_max_s)

        for ii in range(NN):
            for jj in range(MM):
                bpdc[jj][ii], seed = unif(seed, L_min_b, L_max_b)
                fpdc[jj][ii], seed = unif(seed, L_min_f, L_max_f)

        for ii in range(NN):
            for tt in range(TT):
                value, seed = unif(seed, L_min_d, L_max_d)
                dpdc[tt][ii] = 1.0 * int(value)

        # Calculate capacity
        auxf = 0.0

        for ii in range(NN):
            for tt in range(TT):
                if dpdc[tt][ii] > 0.0:
                    fracao = dpdc[tt][ii] / MM
                    for jj in range(MM):
                        auxf += fpdc[jj][ii] + bpdc[jj][ii] * fracao

        aux1 = int(auxf / (MM * TT))

        if (auxf - aux1) > 0.5:
            maq = aux1 + 1.0
        else:
            maq = aux1 * 1.0

        # FORMATAÇÃO DO ARQUIVO DE OUTPUT
        # Número de produtos | Número de períodos
        print(f"{NN} {TT}", file=dat)
        # Número de máquinas
        print(f"{MM}", file=dat)
        # Capacidade calculada acima
        print(f"{maq:10.0f}", file=dat)

        # Tempo de produção | Tempo setup | Custo de setup | Custo de produção
        for jj in range(MM):
            for ii in range(NN):
                print(f"{bpdc[jj][ii]:5.1f} {fpdc[jj][ii]:5.1f} {spdc[jj][ii]:5.1f} {cpdc[jj][ii]:5.1f}", file=dat)

        # Linha com custos de armazenagem
        for ii in range(NN):
            print(f"{hpdc[ii]:5.1f} ", end='', file=dat)
        print("", file=dat)
        
        # Demanda com 1 período por linha
        for tt in range(TT):
            for ii in range(NN):
                print(f"{int(dpdc[tt][ii]):5d} ", end='', file=dat)
            print("", file=dat)

        dat.close()


def roda_problemas(tipo, inicio, fim, nome, tipocap, stcost, sttime):
    """Define o número de produtos (NN), períodos (TT) e máquinas (MM) e chama a função Gera_dados"""
    vetorN = [0, 6, 12, 25, 50]
    for TT in range(6, 19, 6):
        for MM in range(2, 7, 2):
            for id in range(1, 5):
                NN = vetorN[id]
                Gera_dados(nome, NN, MM, TT)


def main():
    roda_problemas("CASBTB", 0, 9, "ABB0", 0.9, 1.0, 1.0)
    roda_problemas("CASATB", 0, 9, "AAB0", 0.9, 10.0, 1.0)
    roda_problemas("CASBTA", 0, 9, "ABA0", 0.9, 1.0, 1.5)
    roda_problemas("CASATA", 0, 9, "AAA0", 0.9, 10.0, 1.5)
    roda_problemas("CNSBTB", 0, 9, "NBB0", 1.0, 1.0, 1.0)
    roda_problemas("CNSATB", 0, 9, "NAB0", 1.0, 10.0, 1.0)
    roda_problemas("CNSBTA", 0, 9, "NBA0", 1.0, 1.0, 1.5)
    roda_problemas("CNSATA", 0, 9, "NAA0", 1.0, 10.0, 1.5)


if __name__ == "__main__":
    main()
