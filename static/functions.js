function invs(name)
{
  document.getElementsByName(name)[0].src = ("/static/" + name + "LogoInverse.png"); 
}

function rmInvs(name)
{
  document.getElementsByName(name)[0].src = ("/static/" + name + "Logo.png");
}
