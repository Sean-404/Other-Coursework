package RockPaperScissors;
import java.util.ArrayList;
import java.util.Scanner;

public class RockPaperScissors {

	public static Scanner s = new Scanner(System.in);
	
	public static void main(String[] args) {
		
		System.out.println("Welcome to Rock Paper Scissors!\nIn this game you will choose between Rock, "
				+ "Paper or Scissors and see if you win against the program!");
		
		while(true) {
			
			ArrayList<String> gameOptions = new ArrayList<String>();
			gameOptions.add("rock");
			gameOptions.add("paper");
			gameOptions.add("scissors");
			
			String userChoice = "";
			
			userChoice = getChoice();
			if(userChoice.equals("quit")){
				System.out.println("Thank you for playing!");
				break;
			}
			if (!gameOptions.contains(userChoice)) {
				System.out.println("Input not valid, try again.");
			}
			
			int rand = (int)(Math.random()*3);
			
			String botMove = "";
			
			if (rand==0) {
				botMove="rock";
			}
			else if (rand==1) {
				botMove="paper";
			} else {
				botMove="scissors";
			}
			
			System.out.println("Bot move: " + botMove);
			
			if (userChoice.equals(botMove)) {
				System.out.println("It's a tie!");
			} else if ((userChoice.equals("rock") && botMove.equals("scissors")) || 
					(userChoice.equals("paper") && botMove.equals("rock")) ||
					(userChoice.equals("scissors") && botMove.equals("paper"))) {
						System.out.println("You win!");
					}
			else {
				System.out.println("You lose!");
			}
		}
		
	}
	
	public static String getChoice() {
		System.out.println("Type your choice (Rock, Paper, Scissors, Quit): ");
		String choice = s.nextLine().toLowerCase();
		return choice;
	}

}
