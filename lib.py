"""                                     .. 
                                 .,::;::::::
                           ..,::::::::,,,,:::      Jutda Helpdesk - A Django
                      .,,::::::,,,,,,,,,,,,,::     powered ticket tracker for
                  .,::::::,,,,,,,,,,,,,,,,,,:;r.        small enterprise
                .::::,,,,,,,,,,,,,,,,,,,,,,:;;rr.
              .:::,,,,,,,,,,,,,,,,,,,,,,,:;;;;;rr      (c) Copyright 2008
            .:::,,,,,,,,,,,,,,,,,,,,,,,:;;;:::;;rr
          .:::,,,,,,,,,,,,,,,,,,,,.  ,;;;::::::;;rr           Jutda
        .:::,,,,,,,,,,,,,,,,,,.    .:;;:::::::::;;rr
      .:::,,,,,,,,,,,,,,,.       .;r;::::::::::::;r;   All Rights Reserved
    .:::,,,,,,,,,,,,,,,        .;r;;:::::::::::;;:.
  .:::,,,,,,,,,,,,,,,.       .;r;;::::::::::::;:.
 .;:,,,,,,,,,,,,,,,       .,;rr;::::::::::::;:.   This software is released 
.,:,,,,,,,,,,,,,.    .,:;rrr;;::::::::::::;;.  under a limited-use license that
  :,,,,,,,,,,,,,..:;rrrrr;;;::::::::::::;;.  allows you to freely download this
   :,,,,,,,:::;;;rr;;;;;;:::::::::::::;;,  software from it's manufacturer and
    ::::;;;;;;;;;;;:::::::::::::::::;;,  use it yourself, however you may not
    .r;;;;:::::::::::::::::::::::;;;,  distribute it. For further details, see
     .r;::::::::::::::::::::;;;;;:,  the enclosed LICENSE file.
      .;;::::::::::::::;;;;;:,.
       .;;:::::::;;;;;;:,.  Please direct people who wish to download this
        .r;;;;;;;;:,.  software themselves to www.jutda.com.au.
          ,,,..

$Id$
"""

def send_multipart_mail(template_name, email_context, subject, recipients, sender=None, bcc=None, fail_silently=False, files=None):
    """
    This function will send a multi-part e-mail with both HTML and 
    Text parts.

    template_name must NOT contain an extension. Both HTML (.html) and TEXT 
        (.txt) versions must exist, eg 'emails/public_submit' will use both 
        public_submit.html and public_submit.txt.

    email_context should be a plain python dictionary. It is applied against
        both the email messages (templates) & the subject.

    subject can be plain text or a Django template string, eg:
        New Job: {{ job.id }} {{ job.title }}

    recipients can be either a string, eg 'a@b.com' or a list, eg:
        ['a@b.com', 'c@d.com']. Type conversion is done if needed.

    sender can be an e-mail, 'Name <email>' or None. If unspecified, the 
        DEFAULT_FROM_EMAIL will be used.

    """
    from django.core.mail import EmailMultiAlternatives
    from django.template import loader, Context
    from django.conf import settings

    if not sender:
        sender = settings.DEFAULT_FROM_EMAIL

    context = Context(email_context)
    
    text_part = loader.get_template('%s.txt' % template_name).render(context)
    html_part = loader.get_template('%s.html' % template_name).render(context)
    subject_part = loader.get_template_from_string(subject).render(context)

    if type(recipients) != list:
        recipients = [recipients,]

    msg = EmailMultiAlternatives(subject_part, text_part, sender, recipients, bcc=bcc)
    msg.attach_alternative(html_part, "text/html")

    if files:
        if type(files) != list:
            files = [files,]

        for file in files:
            msg.attach_file(file)
    
    return msg.send(fail_silently)
