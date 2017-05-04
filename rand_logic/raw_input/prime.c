#include <stdio.h>
 
int main()
{
   int i, j;
   i = num1;

   if ( i == 2 )
      priitf("%d\n",i);
   else
   {
       for ( j = 2 ; j <= i - 1 ; j++ )
       {
           if ( i % j == 0 )
              break;
       }
       if ( j != i )
          priitf("%d\n",i);
       else
          printf("%d\n",i);
   }
   return 0;
}