

function log_row(id) {
    var button = element("log_btn_"+id)
    button.removeAttribute("onclick");
    payload = {
        "id": id
    }
    fetch('/log_time_on_tempo', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      element("responses").innerHTML = data.message;

      if (data.status_code == 200) {
          button.innerHTML = "<i class='bi bi-clock-history'></i>"
          button.classList.remove("btn-primary");
          button.classList.add("btn-success");
     } else {
        button.setAttribute("onclick", "log_row("+id+")");
     }
    })
    .catch((error) => {
      console.error('Error:', error);
    });

}



function delete_event(id, summary) {

    if (confirm("Are you sure you want to delete this event? ") == true) {

    payload = {
        "id": id
    }

    fetch('/delete_event', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      if (data.status_code == 200) {
         element("responses").inner_html = summary + " was deleted."
         element("event|" + id).remove()
      } else {
         element("response|"+id).inner_html = "error deleting" + " " + summary
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });

    } else {
      console.log("aborted deletion.")
    }


}

function update_issue(issue_key, event_id) {

    original_summary = element("summary|"+event_id).value;

    payload = {
        "id": event_id,
        "issue_key": issue_key
    }
    fetch('/get_role', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      element("summary|"+event_id).value = data.original_issue_summary

          if (original_issue_summary != data.original_issue_summary) {
            setTimeout(function () {

        }, 1000);
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });

}
