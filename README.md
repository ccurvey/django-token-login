# django-token-login

I'm tired of remembering passwords.  I've gotten to the point where I just end up saying "change my password" on
many sites, rather than even try to remember.  Then it hit me -- why not use email to just send a one-time token that
can be used to log the user in.  

So here it is.  The token comes in two parts.  When you request a login token, we generate it as two fragements:
one fragment is a hashed version of asctime() and the other is a random integer.  The hashed value is sent in email, the 
second random number is set as a cookie on the requester's browser.

When the user hits the link in the email, we take the two fragments, hash them together, and see if we get the same final
result that was calculated when we sent out the information.  If so, then we are good and we log the user in (and 
delete the hashed value so it can't be used again).

(1) both of those methods are lousy. But we can improve them!
