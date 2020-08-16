#include <stdlib.h>
#include <math.h>
#define SEED 42

double calc_pi()
{
   int niter=1000000;
   double x,y;
   int i,count=0;
   double z;
   double pi;

   srand(SEED);
   count=0;
   for ( i=0; i<niter; i++) {
      x = (double)rand()/RAND_MAX;
      y = (double)rand()/RAND_MAX;
      z = x*x+y*y;
      if (z<=1) count++;
    }
    pi=(double)count/niter*4;
    return pi;
}

