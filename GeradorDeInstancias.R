# Função para gerar dados para diferentes cenários
geraTodas <- function(classe, tipo1, tipo2, tipo3){
  
  T = 12  # Número de períodos de tempo
  
  # Loop para diferentes replicações (r varia de 0 a 4)
  for(r in (0:4)){
    
    # Loop para diferentes quantidades de plantas (M varia de 15 a 20, incrementando de 5)
    for(j in seq(15, 20, by=5)){
      M = j  # Número de plantas
      
      # Loop para diferentes quantidades de produtos (N varia de 70 a 90, incrementando de 10)
      for(i in seq(70, 90, by=10)){
        N = i  # Número de produtos
        n = c(i, T)  # Vetor contendo N e T para escrever no arquivo
        fname = sprintf("%s012%d%d_%d.dat", classe, j, i, r)  # Nome do arquivo de saída
        
        # Inicialização das matrizes e vetores
        custos = matrix(0, (M*N), 4)  # Matriz para armazenar custos (produção, setup, etc.)
        hpdc = numeric(M*N)           # Vetor para custos de estoque
        rpdc = matrix(0, M, N)        # Matriz para relações entre plantas e produtos
        dpdc = matrix(0, T, (M*N))    # Matriz para demandas em cada período
        cap = numeric(M)              # Vetor para capacidades das plantas
        
        # Geração dos custos para cada planta e produto
        for(jj in (1:M)){
          for(ii in (1:N)){
            index = ((jj - 1) * N) + ii  # Índice linear para acessar os vetores
            custos[index, 1] = round(runif(1, 1.0, 5.0), digits=1)                   # Tempo de produção
            custos[index, 2] = round(runif(1, 10.0, 50.0) * tipo1, digits=1)         # Tempo de setup
            custos[index, 3] = round(runif(1, 5.0, 95.0) * tipo2, digits=1)          # Custo de setup
            custos[index, 4] = round(runif(1, 1.5, 2.5), digits=1)                   # Custo de produção
          }
        }
        
        # Geração dos custos de estoque para cada produto em cada planta
        for(jj in (1:M)){
          for(ii in (1:N)){
            index = ((jj - 1) * N) + ii
            hpdc[index] = round(runif(1, 0.2, 0.4), digits=1)  # Custo de manter estoque
          }
        }
        
        # Geração das demandas para cada período, planta e produto
        for(tt in (1:T)){  
          for(jj in (1:M)){
            for(ii in (1:N)){
              index = ((jj - 1) * N) + ii
              dpdc[tt, index] = ceiling(runif(1, 0, 180))  # Demanda entre 1 e 180 unidades
            }
          }
        }
        
        # Custos de transferência entre plantas
        for(jj in (1:M)){
          for(ii in (1:jj)){
            if(ii != jj){
              rpdc[jj, ii] = round(runif(1, 0.2, 0.4), digits=1)
            }
          }
        }
        
        # Cálculo das capacidades para cada planta
        for(jj in (1:M)){
          soma = 0
          for(tt in (1:T)){  
            for(ii in (1:N)){
              index = ((jj - 1) * N) + ii
              # Soma dos custos de produção e setup para cálculo da capacidade
              soma = soma + ((custos[index, 1] * dpdc[tt, index]) + custos[index, 2])
            }
          }
          cap[jj] = ceiling((soma / T) * tipo3)  # Capacidade ajustada pelo tipo3
        }
        
        # Escrita dos dados no arquivo de saída
        write(n, fname, ncolumns = (M*N), append = TRUE, sep = " ")   # Escreve N e T
        write(j, fname, append = TRUE, sep = " ")                     # Escreve M (número de plantas)
        
        # Escreve as capacidades das plantas
        for(jj in (1:M))
          write(cap[jj], fname, append = TRUE, sep = " ")
        
        # Escreve os custos para cada produto em cada planta
        for(jj in (1:M)){
          for(ii in (1:N) )
            write(custos[((jj - 1) * N) + ii, ], fname, append = TRUE, sep = " ")
        }
        
        # Escreve os custos de estoque
        write(hpdc, fname, ncolumns = (M*N), append = TRUE, sep = " ")
        
        # Escreve as demandas para cada período
        for(tt in (1:T)) 
          write(dpdc[tt, ], ncolumns = (M*N), fname, append = TRUE, sep = " ")
        
        # Escreve os custos de transporte entre plantas
        for(jj in (1:M))
          for(ii in (1:jj))
            if(ii != jj)
              write(rpdc[jj, ii], fname, append = TRUE, sep = " ")
      }
    }
  }
}

# Chamadas da função com diferentes classes e parâmetros

# Classe AAA
classe = "AAA"
tipo1 = 1.5
tipo2 = 10
tipo3 = 0.9
geraTodas(classe, tipo1, tipo2, tipo3)

# Classe AAB
classe = "AAB"
tipo1 = 1
tipo2 = 10
tipo3 = 0.9
geraTodas(classe, tipo1, tipo2, tipo3)

# Classe ABA
classe = "ABA"
tipo1 = 1.5
tipo2 = 1
tipo3 = 0.9
geraTodas(classe, tipo1, tipo2, tipo3)

# Classe ABB
classe = "ABB"
tipo1 = 1
tipo2 = 1
tipo3 = 0.9
geraTodas(classe, tipo1, tipo2, tipo3)

# Classe NAA
classe = "NAA"
tipo1 = 1.5
tipo2 = 10
tipo3 = 1
geraTodas(classe, tipo1, tipo2, tipo3)

# Classe NAB
classe = "NAB"
tipo1 = 1
tipo2 = 10
tipo3 = 1
geraTodas(classe, tipo1, tipo2, tipo3)

# Classe NBA
classe = "NBA"
tipo1 = 1.5
tipo2 = 1
tipo3 = 1
geraTodas(classe, tipo1, tipo2, tipo3)

# Classe NBB
classe = "NBB"
tipo1 = 1
tipo2 = 1
tipo3 = 1
geraTodas(classe, tipo1, tipo2, tipo3)
