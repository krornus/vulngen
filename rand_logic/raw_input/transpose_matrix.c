#include <stdio.h>
 
int main()
{
   int i, j, k, l;
   int m[num1][num2] = {num3};
   int n[num1][num2] = {num4};
   
   j= num1;
   i = num2;
 
 
   for (k = 0; k < i; k++)
      for(l = 0; l < j; l++)
         m[k][l] = num5;
 
   for (k = 0; k < i; k++)
      for( l = 0 ; l < j ; l++ )
         n[l][k] = m[k][l];
 
 
   for (k = 0; k < j; k++) {
      for (l = 0; l < i; l++)
         printf("%d\n",n[k][l]);
   } 
   return 0;
}