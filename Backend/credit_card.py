class Transaction():
    
    def __init__(self, id, amount, start_time):
        '''
            Initalized transaction as PENDING
        '''
        self.id = id
        self.amount = amount
        self.start_time = start_time
        self.is_settled = False
    
    def settled(self, end_time):
        '''
            Sets transaction's state to SETTLED
        '''
        self.is_settled = True
        self.end_time = end_time
    
    def money(self, amount):
        '''
            To deal with negative money (instead of $-456, -$456)
        '''
        if amount < 0:
            return f"-${abs(amount)}"
        else:
            return f"${amount}"
    
    def __str__(self):
        '''
            Returns Pending or Settled String depending on the transaction's state
        '''
        pending_transaction = f"{self.id}: {self.money(self.amount)} @ time {self.start_time}"
        if self.is_settled:
            return pending_transaction + f" (finalized @ time {self.end_time})"
        return pending_transaction
        
        
        
        

class CreditSummarizer():
    
    def __init__(self, inputJSON):
        # Only show most recent three pending transactions
        self.transactions = {}
        self.balance = 0
        self.parse_JSON(inputJSON)
    
    def parse_JSON(self, inputJSON):
        '''
            Parses JSON and simulates all events
        '''
        # print(json_dict)
        self.available_credit = inputJSON["creditLimit"]
        
        # Parsing Events
        for event in inputJSON["events"]:
            self.apply_event(event)
  
    
    def apply_event(self, event):
        '''
            Applies given event, which could be:
            
            TXN_AUTHED / PAYMENT_INITIATED (both change available credit but NOT balance)
            TXN_AUTH_CLEARED / PAYMENT_CANCELED (both remove the TXN/PAYMENT from pending transaction list)
            TXN_SETTLED (add to settled list, remove from pending list, potentially updates credit/balance)
            PAYMENT_POSTED (add to settled list, remove from pending list)
        '''
        event_type = event["eventType"]
        if event_type in ["TXN_AUTHED", "PAYMENT_INITIATED"]:
            new_transaction = Transaction(event["txnId"], event["amount"], event["eventTime"])
            self.transactions[new_transaction.id] = new_transaction
            if event_type == "TXN_AUTHED":
                self.available_credit -= new_transaction.amount
            else:
                self.balance += new_transaction.amount
            
        elif event_type in ["TXN_AUTH_CLEARED", "PAYMENT_CANCELED"]:
            deleted_transaction = self.transactions.pop(event["txnId"])
            if event_type == "TXN_AUTH_CLEARED":
                self.available_credit += deleted_transaction.amount
            else:
                self.balance -= deleted_transaction.amount
            
        elif event_type in ["TXN_SETTLED", "PAYMENT_POSTED"]:
            # Update Transaction to Settled
            cur_transaction = self.transactions[event["txnId"]]
            cur_transaction.settled(event["eventTime"])
            if event_type == "TXN_SETTLED":
                # Update Credit Amount if TXN_SETTLED
                self.available_credit += cur_transaction.amount
                cur_transaction.amount = event["amount"]
                self.available_credit -= cur_transaction.amount
                self.balance += cur_transaction.amount
            else:
                self.available_credit -= cur_transaction.amount
        
        else:
            print("Invalid Event")
        # print(event, self.transactions)

    
    
    def get_sorted_transactions(self):
        '''
            Generates sorted list of pending and settled transactions.
            Key is by newest -> oldest in terms of initial_time
        '''
        # Note, could use PriorityQueue instead for O(N) instead of O(NlogN), but too lazy :(
        pending, settled = [], []
        for transaction in self.transactions.values():
            if transaction.is_settled:
                settled.append(transaction)
            else:
                pending.append(transaction)
        sort_key = lambda trans: -trans.start_time 
        pending.sort(key=sort_key)
        settled.sort(key=sort_key)
        return pending, settled
        
        
    
    def summarize(self):
        '''
            Print out available credit and payable balance
            
            Then print out the most recent pending transactions and ALL settled transactions
        '''
        summarized_str = f"Available credit: ${self.available_credit}\nPayable balance: ${self.balance}\n\nPending transactions:\n"
        
        # Return the sorted pending and settled transactions from newest to oldest
        sorted_pending, sorted_settled = self.get_sorted_transactions()
        
        c = 0
        for pending_transaction in sorted_pending:
            if c == 3:
                break
            summarized_str += str(pending_transaction) + "\n"
            c += 1
        
        summarized_str += "\nSettled transactions:\n"
        for settled_transaction in sorted_settled:
            summarized_str += str(settled_transaction) + "\n"
        return summarized_str.rstrip()
        
        