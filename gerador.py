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


def Gera_dados(nome, Produtos, Plantas, Periodos, n_instancias=10):
    """Função principal de leitura dos parâmetros e contrução dos arquivos .dat"""
    # Read parameters from "gdado.dat"
    fname_ent = "gdado.dat"
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
        with open("semente.dat", "r") as arq:
            seed_lines = arq.readlines()
    except IOError:
        print("Erro na abertura do arquivo de dados !!!")
        return 1

    for narq in range(n_instancias):  # CONTROLA O NÚMERO DE INSTÂNCIAS GERADAS!!!
        # Read seed
        tokens = seed_lines[narq].split('=')
        seed = int(tokens[-1].strip())

        fname_dat = f"{nome}{narq}_{Produtos}_{Plantas}_{Periodos}.dat"

        try:
            dat = open(fname_dat, "w")
        except IOError:
            print("Erro na abertura do arquivo de dados !!!")

        # Generate data
        # Inicializar listas
        hpdc = [0.0] * Produtos
        cpdc = [ [0.0]*Produtos for _ in range(Plantas)]
        spdc = [ [0.0]*Produtos for _ in range(Plantas)]
        bpdc = [ [0.0]*Produtos for _ in range(Plantas)]
        fpdc = [ [0.0]*Produtos for _ in range(Plantas)]
        dpdc = [ [0.0]*Produtos for _ in range(Periodos)]
        rpdc = [ [0.0]*Produtos for _ in range(Plantas)]

        for i in range(Produtos):
            hpdc[i], seed = unif(seed, L_min_h, L_max_h)
            for j in range(Plantas):
                cpdc[j][i], seed = unif(seed, L_min_c, L_max_c)
                spdc[j][i], seed = unif(seed, L_min_s, L_max_s)

        for i in range(Produtos):
            for j in range(Plantas):
                bpdc[j][i], seed = unif(seed, L_min_b, L_max_b)
                fpdc[j][i], seed = unif(seed, L_min_f, L_max_f)

        for i in range(Produtos):
            for t in range(Periodos):
                value, seed = unif(seed, L_min_d, L_max_d)
                dpdc[t][i] = 1.0 * int(value)
                
        for j in range(Plantas):
            for i in range(Produtos):
                if i != j:
                    rpdc[j][i], seed = unif(seed, 0.2, 0.4)

        # Calculate capacity
        auxf = 0.0

        for i in range(Produtos):
            for t in range(Periodos):
                if dpdc[t][i] > 0.0:
                    fracao = dpdc[t][i] / Plantas
                    for j in range(Plantas):
                        auxf += fpdc[j][i] + bpdc[j][i] * fracao

        aux1 = int(auxf / (Plantas * Periodos))

        if (auxf - aux1) > 0.5:
            maq = aux1 + 1.0
        else:
            maq = aux1 * 1.0

        # FORMATAÇÃO DO ARQUIVO DE OUTPUT
        # Número de produtos | Número de períodos
        print(f"{Produtos} {Periodos}", file=dat)
        # Número de máquinas
        print(f"{Plantas}", file=dat)
        # Capacidade calculada acima
        print(f"{maq:10.0f}", file=dat)

        # Tempo de produção | Tempo setup | Custo de setup | Custo de produção
        for j in range(Plantas):
            for i in range(Produtos):
                print(f"{bpdc[j][i]:5.1f} {fpdc[j][i]:5.1f} {spdc[j][i]:5.1f} {cpdc[j][i]:5.1f}", file=dat)

        # Linha com custos de armazenagem
        for i in range(Produtos):
            print(f"{hpdc[i]:5.1f} ", end='', file=dat)
        print("", file=dat)
        
        # Demanda com 1 período por linha
        for t in range(Periodos):
            for i in range(Produtos):
                print(f"{int(dpdc[t][i]):5d} ", end='', file=dat)
            print("", file=dat)
            
        for j in range(Plantas):
            for i in range(Produtos):
                if i != j:
                    print(f"{int(rpdc[j][i]):5d} ", end='', file=dat)

        dat.close()


def roda_problemas(tipo, inicio, fim, nome, tipocap, stcost, sttime):
    """Define o número de produtos (NN), períodos (t) e máquinas (MM) e chama a função Gera_dados"""
    # vetorN = [12]
    # for t in range(6, 7):
    #     for MM in range(2, 3):
    #         for id in range(0, 1):
    #             NN = vetorN[id]
    #             Gera_dados(nome, NN, MM, t)
    Gera_dados(nome, 6, 2, 12, n_instancias=1)


def main():
    # roda_problemas("CASBTB", 0, 9, "ABB0", 0.9, 1.0, 1.0)
    # roda_problemas("CASATB", 0, 9, "AAB0", 0.9, 10.0, 1.0)
    # roda_problemas("CASBTA", 0, 9, "ABA0", 0.9, 1.0, 1.5)
    roda_problemas("CASATA", 0, 9, "AAA0", 0.9, 10.0, 1.5)
    # roda_problemas("CNSBTB", 0, 9, "NBB0", 1.0, 1.0, 1.0)
    # roda_problemas("CNSATB", 0, 9, "NAB0", 1.0, 10.0, 1.0)
    # roda_problemas("CNSBTA", 0, 9, "NBA0", 1.0, 1.0, 1.5)
    # roda_problemas("CNSATA", 0, 9, "NAA0", 1.0, 10.0, 1.5)


if __name__ == "__main__":
    main()
