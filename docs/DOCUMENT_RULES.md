# Document Centre Rules

## Pages to add

1. **Prepare Documents**
   - Download the official Medical Approval Request Form.
   - Download the editable cover-letter template.
   - Show print, completion, signature, approval-route, and photo-quality instructions.
   - Show a placeholder for the second official form until it is supplied.

2. **Upload and Check**
   - Upload the completed two-page request form.
   - Upload the signed cover letter after it has followed the required approval route.
   - Upload the medical certificate or report.
   - Upload the second form only after its official template is confirmed.
   - Display checks for each document and an overall status.

3. **Staff Review**
   - Show the uploaded files and automated findings.
   - Allow staff to mark each item as verified, correction required, or rejected.
   - Record a note, reviewer, and review date.

The Prepare and Upload sections can be presented as steps on one student page. The Staff Review page must remain separate and access-controlled.

## Request form checks

### Student section on page 1

- The image/PDF contains the heading `REQUEST FORM FOR MEDICAL APPROVAL`.
- Student name is entered.
- Registration number is entered.
- Medical certificate number is entered.
- Certificate type is selected: Government, Private, Ayurvedic, or Other.
- Medical-centre address and contact details are entered when the certificate is not Government-issued.
- Medical period has From and To dates.
- Number of days is entered and is consistent with the period where possible.
- At least one absence row contains an absent date, activity type, and module.
- Faculty and submission date are entered.
- Student signature is visibly present.
- Assistant Registrar date and signature are visibly present before routing to the University Medical Officer.

### Staff-only sections on page 2

- University Medical Officer observation.
- Certificate-validity decision under KDU by-laws.
- Other recommendations or observations, if applicable.
- University Medical Officer date, signature, and rubber stamp.
- Faculty Board approval/action table entries where required.

These page-2 items are not student omissions during the first upload. Their initial status is `Pending staff completion`.

## Cover-letter checks

- Sender name, registration number, address, and date.
- Primary recipient: University Medical Officer.
- A `Through` route containing the required roles for the student's faculty. Based on the supplied example, these are Dean, Assistant Registrar, and Head of Department. The student must confirm the current official route with the faculty before submission.
- Faculty and university name.
- Salutation.
- Clear subject such as `Reason for absence from lectures`.
- Student name, registration number, programme/intake where required.
- Absence reason, affected date or period, and requested action.
- Polite closing, student signature, typed name, and registration number.
- Visible initials/signatures/stamps from every required routing officer.

The letter is addressed to the University Medical Officer and routed **through** every required approver. This is clearer than listing every role as a separate main recipient.

## Medical certificate checks

- Student identity matches the request form where readable.
- Issue date and recommended leave/absence period are visible.
- Medical-practitioner or medical-centre name is visible.
- Signature and official stamp appear present.
- Certificate or report number is present when the document uses one.

The system should not extract or display a diagnosis unless the university explicitly requires it. It should not judge medical validity.

## Statuses

- `File missing` - a required upload was not supplied.
- `Unreadable` - OCR could not read enough text or image quality is inadequate.
- `Needs correction` - a required student-completed item appears missing.
- `Ready for staff review` - automated and student-confirmed checks passed.
- `Pending staff completion` - a staff-only section has not yet been completed.
- `Staff verified` - an authorized reviewer has checked the original documents.
- `Rejected` - an authorized reviewer rejected the submission and recorded a reason.

## Privacy and security

- Accept only PDF, JPG, JPEG, and PNG.
- Limit file size and page count.
- Validate the actual file type, not only the filename.
- Encrypt stored files and restrict them by role.
- Do not place real uploads in GitHub.
- Delete temporary OCR images after checking.
- Keep an audit log for staff decisions.
- Use fictional or fully redacted documents for demonstrations.
