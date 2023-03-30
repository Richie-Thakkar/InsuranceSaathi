function verifyPassword() {
  //Fetcg values of passwrod and confirm password from DOM
    var pw = document.getElementById("pw").value;
    var p = document.getElementById("pw1").value;
    //Minimum length checking  
    if (pw.length < 8) {
      alert("Password length must be atleast 8 characters");
      event.preventDefault();
      return false;
    }
    //Maximum length checking 
    if (pw.length > 15) {
      alert("Password length must not exceed 15 characters");
      event.preventDefault();
      return false;
    }
    //Check if password and confirm password fields have the same Strings
    if (p != pw) {
      alert("Passwords did not match");
      event.preventDefault();
      return false;
    }
    
    else {
      //Iterate the whole string using a for loop to check occurence of a special character
      for(let i=0; i<p.length; i++)
    {
      if(p[i]==='@' || p[i]==='_' || p[i]==='-')
      {
        alert("Account created successfully");
        return true;
      }
    }
      alert("Password must contain at least one of the special characters from @ or _  or -");
      event.preventDefault();
      return false;
    }
  }