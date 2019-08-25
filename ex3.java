public Class lacoRepetido{
    public static void main(String[] args){
        java.util.Scanner sc = new java.util.Scanner(System.in);
        int x = sc.nextInt();
        int fatorial = 1;
        while (x>=1){
            fatorial = fatorial*x;
            x = x-1;
        }
        System.out.println(fatorial);
    }
}