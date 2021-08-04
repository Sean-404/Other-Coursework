
public class BalanceInquiry extends Transaction {
    public BalanceInquiry(int accountNo, Screen screen, BankDatabase database) {
    	super(accountNo, screen, database);

    }

    @Override
    public void execute() {
    	Screen screen = getScreen();
    	BankDatabase database = getBankDatabase();

    	double availableBalance = database.getAvailableBalance(getAccountNo());
    	// double availableBalance = database.getAvailableBalance(accountNo);

    	double totalBalance = database.getTotalBalance(getAccountNo());
    	// double totalBalance = database.getTotalBalance(accountNo);

    	screen.displayMessageLine("");
    	screen.displayMessageLine("Balance Data : ");

    	screen.displayMessage(" - Available Balance : ");
    	screen.displayAmount(availableBalance);
    	screen.displayMessageLine("");

    	screen.displayMessage(" - Total Balance :     ");
    	screen.displayAmount(totalBalance);
    	screen.displayMessageLine("");
    }
}
