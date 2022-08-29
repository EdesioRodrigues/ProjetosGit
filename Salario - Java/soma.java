public class soma {
  public static void main(String[]args){
    int quantidadeAnos = 5;
    int horasTrabalhadas = 40;
    int valorHora = 50;
    int salario = 0;

    if (quantidadeAnos <= 1){
        salario = 1500 + (valorHora * horasTrabalhadas);
    }
    else if((quantidadeAnos > 1) &&  (quantidadeAnos < 3)){
        salario = 2000 + (valorHora * horasTrabalhadas);
    }
    else {
        salario = 3000 + (valorHora * horasTrabalhadas);
    }

    System.out.println(salario);
  }
}
