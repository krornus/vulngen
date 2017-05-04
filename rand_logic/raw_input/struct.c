#include <stdio.h>
 
struct s
{
    float i;
    char *j;
};
 
int main()
{
   struct s k;
   char l[] = "string";   
 
   k.i = float1;
   k.j = l;
 
   printf("%f\n", k.i);
   printf("%s\n", k.j);
 
   return 0;
}