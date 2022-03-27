function addOrUpdateUrlParam(name, value)
{
  var href = window.location.href;
  var regex = new RegExp("[&\\?]" + name + "=");
  if(regex.test(href))
  {
    // regex = new RegExp("([&\\?])" + name + "=\\d+");
      regex = new RegExp("([&\\?])" + name + "=.*?(?=&|$)");
    window.location.href = href.replace(regex, "$1" + name + "=" + value);
    //   window.location.href = href.replace(regex, "");
    //   window.location.href += "&" + name + "=" + value;
  }
  else
  {
    if(href.indexOf("?") > -1)
      window.location.href = href + "&" + name + "=" + value;
    else
      window.location.href = href + "?" + name + "=" + value;
  }
}