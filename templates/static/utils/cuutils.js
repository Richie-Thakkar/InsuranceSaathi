(function() {
    emailjs.init("RTrBhud1dn1UdczWF");
})();
function sendmail()
{
emailjs.send("service_za2208f","template_crpwmkv",{
    from_name: document.getElementById("name").value,
    email_id: document.getElementById("em").value,
    title:document.getElementById("qry").value ,
    message: document.getElementById("desc").value,
    })
    .then(function(res)
    {
alert("Query Sent Succesfully!");
    }
    );
}
