/* Gerador dos exemplos do artigo do European */
#include<stdio.h>
#include<string.h>
#include<math.h>
// #include<sys/times.h>
#include<sys/types.h>


#define  MAX_T		   20
#define  MAX_M		    8
#define  MAX_N		   52

double    maq;
double    hpdc[MAX_N], dpdc[MAX_T][MAX_N];
double    fpdc[MAX_M][MAX_N], spdc[MAX_M][MAX_N];
double    cpdc[MAX_M][MAX_N];
double    bpdc[MAX_M][MAX_N];
double	  I[MAX_T][MAX_N],
          x[MAX_T][MAX_M][MAX_N];




double unif(long int *seed, double low, double high)
{
  double   unif_ret;
  long int m,a,b,c, k;
  double   value_0_1;

  m = 2147483647;
  a = 16807;
  b = 127773;
  c = 2836;

  k = *seed/b;
  *seed = a * (*seed % b) - k * c;
  if (*seed <0)
    *seed = *seed + m;
  value_0_1 = (double) *seed/m;
  unif_ret = low + value_0_1 * (high - low);
  return (unif_ret);
}



int Gera_dados (char nome[10], int NN, int MM, int TT)
{
  int    narq          ;
  char   fname_dat[30] ;
  FILE  *dat           ;
  FILE  *arq           ;
  char   fname_ent[15] ;
  double L_min_s, L_max_s,
         L_min_c, L_max_c,
         L_min_h, L_max_h,
         L_min_d, L_max_d,
         L_min_f, L_max_f,
         L_min_b, L_max_b,
         fracao, auxf;
  long int    seed;
  int    aux1, ii, jj, tt;
  double max_f, max_b;

/* Le do arquivo gdado.dat os parametros que serao utilizados na geracao
   dos problemas testes                                                   */

  sprintf(fname_ent,"../gdado.dat");
  if ((arq = fopen (fname_ent, "r")) == NULL){
    printf ("Erro na abertura do arquivo de dados !!!\n");
    return(1);
  }

  fscanf( arq, "%*s" );
  fscanf( arq, "%*s %*s %lf", &L_min_s );
  fscanf( arq, "%*s %*s %lf", &L_max_s );
  fscanf( arq, "%*s %*s %lf", &L_min_c );
  fscanf( arq, "%*s %*s %lf", &L_max_c );
  fscanf( arq, "%*s %*s %lf", &L_min_h );
  fscanf( arq, "%*s %*s %lf", &L_max_h );
  fscanf( arq, "%*s %*s %lf", &L_min_d );
  fscanf( arq, "%*s %*s %lf", &L_max_d );

  fscanf (arq, "%*s");
  fscanf( arq, "%*s %*s %lf", &L_min_b );
  fscanf( arq, "%*s %*s %lf", &L_max_b );
  fscanf( arq, "%*s %*s %lf", &L_min_f );
  fscanf( arq, "%*s %*s %lf", &L_max_f );

//  fscanf( arq, "%*s %*s %d" , &L_NP);

  fclose(arq);

  /* inicio da geracao dos dados - gera 10 problemas para cada NxMxT dado */

  if ((arq = fopen ("../semente.dat", "r")) == NULL){
    printf ("Erro na abertura do arquivo de dados !!!\n");
    return(1);
  }

  for(narq=0;narq<10;narq++){

    fscanf(arq, "%*s %*s %d",&seed);
    sprintf(fname_dat,"%s%d_%d_%d_%d.dat",nome,narq,NN,MM,TT);

    if ((dat = fopen (fname_dat, "w")) == NULL) {
     printf ("Erro na abertura do arquivo de dados !!!\n");
     return(1);
    }

    /* geracao dos dados */

    for(ii=1;ii<=NN;ii++){
      hpdc[ii] = unif(&seed,L_min_h,L_max_h);
      for(jj=1;jj<=MM;jj++){
        cpdc[jj][ii] = unif(&seed,L_min_c,L_max_c);
        spdc[jj][ii] = unif(&seed,L_min_s,L_max_s);
      }
    }

    for(ii=1;ii<=NN;ii++)
      for(jj=1;jj<=MM;jj++){
        bpdc[jj][ii] = unif(&seed,L_min_b,L_max_b);
        fpdc[jj][ii] = unif(&seed,L_min_f,L_max_f);
      }


    for(ii=1;ii<=NN;ii++)
      for(tt=1;tt<=TT;tt++)
        dpdc[tt][ii] = 1.0* ((int) (unif(&seed,L_min_d,L_max_d)));

  /* Calculo da capacidade */

  auxf = 0.0;

  for(ii=1;ii<=NN;ii++)
    for(tt=1;tt<=TT;tt++)
      if (dpdc[tt][ii]>0.0){
        fracao = dpdc[tt][ii]/MM;
        for(jj=1;jj<=MM;jj++)
          auxf += fpdc[jj][ii] + bpdc[jj][ii]*fracao;
      }

  aux1 = (int)(auxf/(MM*TT)); /*politica lote por lote */

  if ((auxf - aux1) > 0.5)
    maq = 1.0*aux1+1.0;
  else
    maq = 1.0*aux1;

  /* Fim do calculo da capacidade */


  /* Escrevendo no arquivo de saida */

  fprintf(dat,"%d %d\n",NN, TT);
  fprintf(dat,"%d\n",MM);

  fprintf(dat,"%10.0lf\n",maq);

  for(jj=1;jj<=MM;jj++)
    for(ii=1;ii<=NN;ii++){
      fprintf(dat,"%5.1lf %5.1lf ",bpdc[jj][ii],fpdc[jj][ii]);
      fprintf(dat,"%5.1lf %5.1lf \n",spdc[jj][ii],cpdc[jj][ii]);
    }
  for(ii=1;ii<=NN;ii++)
    fprintf(dat,"%5.1lf ",hpdc[ii]);
  fprintf(dat,"\n");


  if(NN<=15){
   for(tt=1;tt<=TT;tt++){
    for(ii=1;ii<=NN;ii++)
     fprintf(dat,"%5d ",(int)(dpdc[tt][ii]));
    fprintf(dat,"\n");
   }
  }
  else{
   for(tt=1;tt<=TT;tt++){
    for(ii=1;ii<=15;ii++)
     fprintf(dat,"%5d ",(int)(dpdc[tt][ii]));
    fprintf(dat,"\n");
   }

   for(tt=1;tt<=TT;tt++){
    for(ii=16;ii<=NN;ii++)
     fprintf(dat,"%5d ",(int)(dpdc[tt][ii]));
    fprintf(dat,"\n");
   }
  }

  fclose(dat);
  }
  fclose(arq);
}



void roda_problemas(char tipo[10],int inicio, int fim, char nome[10], double tipocap, double stcost, double sttime)
{
  int    vetorN[5];
  int    erro, TT, MM, id, NN;

  vetorN[1] = 6; vetorN[2] = 12; vetorN[3] = 25; vetorN[4] = 50;

  for(TT=6;TT<=18;TT=TT+6)
    for(MM=2;MM<=6;MM=MM+2)
      for(id=1;id<=4;id++){
        NN = vetorN[id];
        erro = Gera_dados(nome,NN,MM,TT);
      }
}


int main(void)
{
 FILE *saida;

 roda_problemas("CASBTB",0,9,"ABB0",0.9, 1.0,1.0);

 roda_problemas("CASATB",0,9,"AAB0",0.9, 10.0,1.0);
 
 roda_problemas("CASBTA",0,9,"ABA0",0.9, 1.0,1.5);

 roda_problemas("CASATA",0,9,"AAA0",0.9, 10.0,1.5);
 
 roda_problemas("CNSBTB",0,9,"NBB0",1.0, 1.0,1.0);

 roda_problemas("CNSATB",0,9,"NAB0",1.0, 10.0,1.0);

 roda_problemas("CNSBTA",0,9,"NBA0",1.0, 1.0,1.5);

 roda_problemas("CNSATA",0,9,"NAA0",1.0, 10.0,1.5);

 return(0);
}
