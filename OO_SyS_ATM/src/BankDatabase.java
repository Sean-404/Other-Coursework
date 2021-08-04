
public final class BankDatabase {
    private Account[] arrayAccounts;

    public BankDatabase() {
        arrayAccounts = new Account[2];

        arrayAccounts[0] = new Account(3333, 3333, 1000.00, 2000.00); // sample hard coded data for tests
        arrayAccounts[1] = new Account(7777, 7777, 200.00, 200.00);   // sample . .
    }

    // private method not discovered in design stage
    private Account getAccount(int accountNo) {
        for (Account currentAccount : arrayAccounts) {
            if (currentAccount.getAccountNo() == accountNo) {
                return currentAccount;
            }
        }

        return null;
    }

    public boolean authenticateUser(int userAccountNo, int userPIN) {
        Account userAccount = getAccount(userAccountNo);

        if (userAccount != null) {
            return userAccount.validatePIN(userPIN);
        }
        else {
            return false;
        }
    }

    public double getAvailableBalance(int userAccountNo) {
        return getAccount(userAccountNo).getAvailableBalance();
    }

    public double getTotalBalance(int userAccountNo) {
        return getAccount(userAccountNo).getTotalBalance();
    }

    public void credit(int userAccountNo, double amount) {
        getAccount(userAccountNo).credit(amount);
    }

    public void debit(int userAccountNo, double amount) {
        getAccount(userAccountNo).debit(amount);
    }
}
