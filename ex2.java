public Class notadeAula{
    public static void main(String[] args){
        java.util.Scanner sc = new java.util.Scanner(System.in);
        double notap1 = sc.nextDouble();
        double notap2 = sc.nextDouble();
        if ((notap1+notap2)/2>5){
            System.out.println("Aprovado");
        }else{
            System.out.println("Reprovado");
        }
    }
}