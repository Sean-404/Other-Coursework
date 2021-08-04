
public class Withdraw extends Transaction {
    private int amount;
    private KeyPad keyPad;
    private CashSlot cashSlot;

    private final int ABORT = 6;

    public Withdraw(int accountNo, Screen screen, BankDatabase database, KeyPad keyPad, CashSlot cashSlot) {
    	super(accountNo, screen, database);

        this.keyPad = keyPad;
        this.cashSlot = cashSlot;
    }

    @Override
    public void execute() {
        boolean cashDispense = false;
        double availableBalance;

        Screen screen = getScreen();
        BankDatabase database = getBankDatabase();

        do {
            amount = displayAmountsMenu();

            if (amount != ABORT) {
                availableBalance = database.getAvailableBalance(getAccountNo());
                // availableBalance = database.getAvailableBalance(accountNo);

                if (amount <= availableBalance) {
                    if (cashSlot.isSufficientCashAvailable(amount)) {
                        database.debit(getAccountNo(), amount);
                        // database.debit(accountNo, amount);

                        cashSlot.dispenseCash(amount);
                        cashDispense = true;

                        screen.displayMessageLine("");
                        screen.displayMessageLine("Please take your cash now.");
                    }
                    else {
                        screen.displayMessageLine("");
                        screen.displayMessageLine("Insufficient cash available in the ATM. Please choose a smaller amount.");
                    }
                }
                else {
                    screen.displayMessageLine("");
                    screen.displayMessageLine("Insufficient funds in your account. Please choose a smaller amount.");
                }
            }
            else {
                screen.displayMessageLine("");
                screen.displayMessageLine("Aborting Transaction . .");
                return;
            }
        } while (!cashDispense);
    }

    private int displayAmountsMenu() {
        int userChoice = 0;
        int[] amounts = { 0, 20, 40, 60, 100, 200 };

        Screen screen = getScreen();

        while (userChoice == 0) {
            screen.displayMessageLine("");
            screen.displayMessageLine("Withdraw Menu :");
            screen.displayMessageLine("1 - £20");
            screen.displayMessageLine("2 - £40");
            screen.displayMessageLine("3 - £60");
            screen.displayMessageLine("4 - £100");
            screen.displayMessageLine("5 - £200");
            screen.displayMessageLine("6 - Abort Transaction");
            screen.displayMessageLine("");
            screen.displayMessage("Choose a Withdraw Amount : ");

            int input = keyPad.getInput();

            switch (input) {
                case 1:
                case 2:
                case 3:
                case 4:
                case 5: {
                        userChoice = amounts[input];
                        break;
                    }
                case ABORT: {
                        userChoice = ABORT;
                        break;
                    }
                default: {
                        screen.displayMessageLine("");
                        screen.displayMessageLine("Wrong Selection. Please Try Again.");
                        break;
                    }
            }
        }

        return userChoice;
    }
}
