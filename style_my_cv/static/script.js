function printDiv(divName) {
     var printContents = document.getElementById(divName).innerHTML;
     var originalContents = document.body.innerHTML;

     document.body.innerHTML = printContents;

     window.print();

}     document.body.innerHTML = originalContents;

function presentCheck() {
     if (document.querySelector("input[name='present']").checked == true) {
         document.querySelector("input[name='dateend']").disabled = true;
     }
     else {
         document.querySelector("input[name='dateend']").disabled = false;
     }
 }

 function jobCheck() {
      document.querySelector("button[name='change']").disabled = false;
 }

 function AreYouSure() {
     return confirm("Are You Sure?")
 }