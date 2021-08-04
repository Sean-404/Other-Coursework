
public class ATM {
    private boolean userAuthenticate;
    private int accountNo;
    private Screen screen;
    private KeyPad keyPad;
    private CashSlot cashSlot;
    private DepositSlot depositSlot;
    private BankDatabase database;

    private final int BALANCE_INQUIRY = 1;
    private final int WITHDRAWAL = 2;
    private final int DEPOSIT = 3;
    private final int EXIT = 4;

    public ATM() {
        userAuthenticate = false;
        accountNo = 0;
        screen = new Screen();
        keyPad = new KeyPad();
        cashSlot = new CashSlot();
        depositSlot = new DepositSlot();
        database = new BankDatabase();
    }

    public void run() {
        while (true) {
            while (!userAuthenticate) {
                screen.displayMessageLine("");
                screen.displayMessageLine("Welcome!");
                authenticateUser();
            }

            performTransactions();
            userAuthenticate = false;
            accountNo = 0;

            screen.displayMessageLine("");
            screen.displayMessageLine("Thank You!");
        }
    }

    private void authenticateUser() {
        screen.displayMessageLine("");
        screen.displayMessage("Please enter your Account No : ");
        int accountNo = keyPad.getInput();

        screen.displayMessageLine("");
        screen.displayMessage("Please enter your PIN : ");
        int pin = keyPad.getInput();

        userAuthenticate = database.authenticateUser(accountNo, pin);

        if (userAuthenticate) {
            this.accountNo = accountNo;
        }
        else {
            screen.displayMessageLine("Wrong Account No or PIN. Please try again!");
        }
    }

    private void performTransactions() {
        Transaction transaction = null;
        boolean userExit = false;

        while (!userExit) {
            int menuSelection = displayMainMenu();

            switch (menuSelection) {
                case BALANCE_INQUIRY:
                case WITHDRAWAL:
                case DEPOSIT: {
                        transaction = startTransaction(menuSelection);
                        transaction.execute();
                        break;
                    }
                case EXIT: {
                        screen.displayMessageLine("");
                        screen.displayMessageLine("Exiting System . .");
                        userExit = true;
                        break;
                    }
                default: {
                        screen.displayMessageLine("");
                        screen.displayMessageLine("You did not enter a valid selection. Please try again!");
                        break;
                    }
            }
        }
    }

    private int displayMainMenu() {
        screen.displayMessageLine("");
        screen.displayMessageLine("Main Menu :");
        screen.displayMessageLine("1 - View Balance");
        screen.displayMessageLine("2 - Withdraw Cash");
        screen.displayMessageLine("3 - Deposit Funds");
        screen.displayMessageLine("4 - Exit");
        screen.displayMessageLine("");
        screen.displayMessage("Enter Choice : ");

        return keyPad.getInput();
    }

    private Transaction startTransaction(int type) {
        Transaction transaction = null;

        switch (type) {
            case BALANCE_INQUIRY: {
            		transaction = new BalanceInquiry(accountNo, screen, database);
                    break;
                }
            case WITHDRAWAL: {
            		transaction = new Withdraw(accountNo, screen, database, keyPad, cashSlot);
                    break;
                }
            case DEPOSIT: {
            		transaction = new Deposit(accountNo, screen, database, keyPad, depositSlot);
                    break;
                }
        }

        return transaction;
    }
}
