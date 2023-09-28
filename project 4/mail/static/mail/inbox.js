document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_mail);

  // By default, load the inbox
  load_mailbox('inbox');
});

function send_mail(event) {
  event.preventDefault()

  //get data from form
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  //send data to backend
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      console.log(result);
      load_mailbox('sent');


    });

}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


  //get emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    //create table with emails
    console.log(mailbox)
    const table = document.createElement('table');
    table.setAttribute("class", "table")
    document.querySelector('#emails-view').append(table);
    emails.forEach(email => {

      if (mailbox == 'sent')
         sender = `To: ${email.recipients}`;
      else
         sender = `${email.sender}`;
      const row = document.createElement('tr')
      row.innerHTML = `
      <td>${sender}</td>
      <td>${email.subject}</td>
      <td>${email.timestamp}</td>`


      if (email.read == false)
        row.className = 'font-weight-bold'
      else
        row.className = 'font-weight-normal'

      row.addEventListener('click', () => {
        load_email(email.id, mailbox);
        });

      document.querySelector('table').append(row);

    })
    .catch(error => {
      console.log('Error:', error)
    });
  });

}

function load_email(id, mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  //get email
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      console.log(email);
      document.querySelector('#email-view').innerHTML = `
      <h5><strong>From: </strong>${email.sender}</h5>
      <h5><strong>To: </strong>${email.recipients}</h5>
      <h5><strong>Subject: </strong>${email.subject}</h5>
      <h5><strong>Timestamp: </strong>${email.timestamp}</h5>
      <hr>
      <textarea disabled class="form-control" id="exampleFormControlTextarea1" rows="3">${email.body}</textarea>
      <hr>`

      //change to read
      if (email.read == false)
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })

      //reply to email
      const reply_btn = document.createElement('botton');
      reply_btn.setAttribute("class", "btn btn-info mr-1");
      reply_btn.innerHTML = "Reply";
      reply_btn.addEventListener('click', () => {
        compose_email();

        document.querySelector('#compose-recipients').value = email.sender;
        let subject = email.subject;
        if (subject.includes("Re:", 0))
          subject = email.subject;
        else
          subject = 'Re: ' + email.subject;
        document.querySelector('#compose-subject').value = subject;
        document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;

      });

      if (mailbox != "sent")
        document.querySelector('#email-view').append(reply_btn);

      //archive email
      const archive_btn = document.createElement('botton');
      archive_btn.className = email.archived ? "btn btn-secondary padding-left" : "btn btn-light";
      archive_btn.innerHTML = email.archived ? "Unarchive" : "Archive" ;

      archive_btn.addEventListener('click', () => {
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: !email.archived
          })
        })
        .then(() => {load_mailbox('archive')})

      });

      if (mailbox != "sent")
        document.querySelector('#email-view').append(archive_btn);
  });



}











emails.forEach(email => {
  const grid_line = document.createElement('div');
  const recipientSender_field = document.createElement('span');
  const subject_field = document.createElement('span');
  const timestamp_field = document.createElement('span');
  const archivebutton = document.createElement('button');

  subject_field.innerHTML = `${email.subject}`;
  timestamp_field.innerHTML = `${email.timestamp}`;

  timestamp_field.setAttribute('class', 'stamp');

  if (mailbox == 'sent') {
      grid_line.setAttribute('class', 'mailUnit');
      recipients = separatingRecipients(email.recipients);
      recipientSender_field.innerHTML = `To: ${recipients}`;
  }
  else {
      recipientSender_field.innerHTML = `From: ${email.sender}`;
      if (email.read == true)
          grid_line.setAttribute('class', 'mailUnit4 readMessage');
      else
          grid_line.setAttribute('class', 'mailUnit4 unreadMessage');

      if (mailbox == 'inbox')
          archivebutton.innerText = 'Archive';
      else
          archivebutton.innerText = 'Unzip';

      archivebutton.className = 'arcButton btn-outline-primary';
  }

  const linkdiv = document.createElement('div');
  linkdiv.setAttribute('class', 'linkdiv');

  grid_line.append(recipientSender_field, subject_field, timestamp_field, linkdiv);
  if (mailbox != 'sent')
      grid_line.append(archivebutton);

  maingrid.append(grid_line);

  linkdiv.addEventListener('click', () => {
      load_email(email.id, mailbox);
      });

  archivebutton.addEventListener('click', () => {
      archive_email(email.id, email.archived, mailbox);
      });
});
