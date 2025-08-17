from fastapi import APIRouter

router = APIRouter()

@router.get("/email-body-html-template", summary="Get HTML email body template")
def get_email_body_html_template():
    return """
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #2e7d32;">Hello,</h2>
        <p style="font-size: 14px;">
          {{message}}
        </p>
        <p style="margin-top: 20px; font-size: 13px; color: #555;">
          Regards,<br>
          <b>JagatRakshak Team</b>
        </p>
      </body>
    </html>
    """
     
