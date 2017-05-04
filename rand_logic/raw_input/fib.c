#include <stdio.h>
 
int main()
{
   int i;
   int j;
   int k;
   int l;
   int m;
 
   j = 0;
   k = 1;
   i = num1;
 
 
 
   for ( m = 0 ; m < i; m++ )
   {
      if ( m <= 1 )
         l = m;
      else
      {
         l = j + k;
         j = k;
         k = l;
      }
      printf("%d\n",l);
   }
 
   return 0;
}