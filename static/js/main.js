function clearPasswordResult() {
  window.addEventListener("pagehide", (e) => {
     e.preventDefault();
     document.querySelector("#password-value").value = "";
  });
}

function addAccountFields(){
  const category = document.querySelector('#category');
  category.addEventListener('change', (e) => {
       if (e.currentTarget == 'Bill') {
           accountFields()
       }
  })
}

function accountFields(){
   const accountItems = document.createElement('div');
   const amountElm = document.createElement('input');
   const dueDateElm = document.createElement('input');
   const priorityElm = document.createElement('select');
   const highOptionElm = document.createElement('option');
   const medOptionElm = document.createElement('option');
   const lowOptionElm = document.createElement('option');
   const autoPayElm = document.createElement('div');
   const autoPaySwitch = document.createElement('div');
   accountItems.setAttribute('id', 'account-items');
   amountElm.setAttribute('type', 'text');
   amountElm.setAttribute('name', 'amount');
   amountElm.setAttribute('placeholder', 'Amount');
   amountElm.setAttribute('required', '');
   dueDateElm.setAttribute('type', 'date');
   dueDateElm.setAttribute('name', 'due-date');
   dueDateElm.setAttribute('placeholder', 'Due date');
   dueDateElm.setAttribute('required', '');
   priorityElm.setAttribute('name', 'priority');
   priorityElm.setAttribute('id', 'priority');
   autoPayElm.setAttribute('id', 'autopay');
   autoPaySwitch.setAttribute('id', 'autopay-switcher');
   autoPaySwitch.setAttribute('data-value', 0);
   highOptionElm.setAttribute('value', 'High');
   medOptionElm.setAttribute('value', 'Medium');
   lowOptionElm.setattribute('value', 'Low');
   const highOptionText = document.createTextNode('High');
   const medOptionText = document.createTextNode('Medium');
   const lowOptionText = document.createTextNode('Low');
   highOptionElm.append(highOptionText);
   medOptionElm.append(medOptionText);
   lowOptionElm.append(lowOptionText);
   priorityElm.append(highOptionElm);
   priorityElm.append(medOptionElm);
   priorityElm.append(lowOptionElm);
   autoPayElm.append(autoPaySwitch);
   accountItems.append(amountElm);
   accountItems.append(dueDateElm);
   accountItems.append(priorityElm);
   accountItems.append(autoPayElm);
   document.querySelector('#additional-items').append(accountItems);
}

clearPasswordResult();
