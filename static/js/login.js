var signIn = document.getElementById('signIn');
var signUp = document.getElementById('signUp');
var signUpVisible = document.getElementById("signUp-visible");
var signUpHidden = document.getElementById("signUp-hidden");
var signInVisible = document.getElementById("signIn-visible");
var signInHidden = document.getElementById("signIn-hidden");

signIn.onclick = function(){
  signIn.style.width = '500px';
  signUp.style.width = '100px';
  signInVisible.className = 'hidden';
  signInHidden.className = 'hidden-animation';
  
  //Need to add if statement to check of other visible/hidden has already been clicked. 
  if(signUpVisible.classList.contains('hidden')){
    signUpHidden.className = 'hidden';
    signUpVisible.className = 'visible hidden-animation';
  }
}
signUp.onclick = function(){
  signIn.style.width = '100px';
  signUp.style.width = '500px';
  signUpVisible.className = 'hidden';
  signUpHidden.className = 'visible hidden-animation';
  
  //Need to add if statement to check of other visible/hidden has already been clicked. 
  if(signInVisible.classList.contains('hidden')){
    signInHidden.className = 'hidden';
    signInVisible.className = 'visible hidden-animation';
  }
}