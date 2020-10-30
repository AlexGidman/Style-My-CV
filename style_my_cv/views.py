from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from time import sleep

from style_my_cv.auth import login_required
from style_my_cv.db import get_db
from style_my_cv.helpers import (
    convert_to_list_of_dicts, cv_date_format, convert_to_dict
)


bp = Blueprint('views', __name__)


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Index page - hosts the formatted CV depending on the 'tag' attribute on the page"""

    db = get_db()
    user_id = session["user_id"]

    # Details in list   
    details = convert_to_dict(db.execute(
            "SELECT * FROM details WHERE user_id = ?", (user_id,)).fetchone())

    # Skills in list
    skills = convert_to_list_of_dicts(db.execute(
        "SELECT * FROM skills WHERE user_id = ?", (user_id,)))

    # Jobs in list
    employment = convert_to_list_of_dicts(db.execute(
        "SELECT * FROM employment WHERE user_id = ? ORDER BY datestart DESC", (user_id,)))
    cv_date_format(employment)

    # Education in list
    education = convert_to_list_of_dicts(db.execute(
        "SELECT * FROM education WHERE user_id = ? ORDER BY datestart DESC", (user_id,)))
    cv_date_format(education)

    # Tags from Skills, Employment, & Education
    # TODO: Create Tags Table and use this instead! Perhaps get_tags function...
    tags = []
    for skill in skills:
        if skill['tag'] not in tags and skill['tag'] != '':
            tags.append(skill['tag'])
    for job in employment:
        if job['tag'] not in tags and job['tag'] != '':
            tags.append(job['tag'])
    for course in education:
        if course['tag'] not in tags and course['tag'] != '':
            tags.append(course['tag'])

    # Tag for CV Generation
    tag = request.form.get('tag') if request.method == "POST" else None

    return render_template("views/index.html", details=details,
                            skills=skills, tags=tags, tag=tag,
                            employment=employment, education=education)


@bp.route("/details", methods=["GET", "POST"])
@login_required
def details():
    """Details page for adding and updating profile details"""

    db = get_db()
    user_id = session["user_id"]
    details = convert_to_dict(db.execute(
        "SELECT * FROM details WHERE user_id = ?", (user_id,)).fetchone())

    if request.method == "POST":
        # assign detail values
        summary = request.form.get("summary")
        name = request.form.get("name")
        address = request.form.get("address")
        phone = request.form.get("phone")
        email = request.form.get("email")
        linkedin = request.form.get("linkedin")
        website = request.form.get("website")

        # Check database for users previous details - insert if false, update if true
        if not details:
            db.execute("INSERT INTO details (user_id, summary, name, address, phone, email, linkedin, website) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (user_id, summary, name, address, phone, email, linkedin, website))
            db.commit()
            flash("New details added!")
            return redirect(url_for('views.index'))
        else:
            db.execute("UPDATE details SET summary = ?, name = ?, address = ?, phone = ?, email = ?, linkedin = ?, website = ? WHERE user_id = ?",
                       (summary, name, address, phone, email, linkedin, website, user_id))
            db.commit()
            flash("Details updated!")
            return redirect(url_for('views.index'))

    return render_template("views/details.html", details=details)


@bp.route("/employment", methods=["GET", "POST"])
@login_required
def employment():

    db = get_db()
    user_id = session["user_id"]
    if request.method == "GET":
        # Pull all employment history for user to pass to emploment.html
        employment = convert_to_list_of_dicts(db.execute(
            "SELECT * FROM employment WHERE user_id = ?", (user_id,)))
        return render_template("views/employment.html", employment=employment)

    if request.method == "POST":
        # DELETE entry
        if request.form['submit'] == "delete":
            job_id = int(request.form.get("job_id"))
            db.execute("DELETE FROM employment WHERE id = ?", (job_id,))
            db.commit()
            flash("Employment Entry Deleted!")
            return redirect(url_for('views.employment'))

        # UPDATE & ADD entry
        # Request values from form
        position = request.form.get("position")
        company = request.form.get("company")
        location = request.form.get("location")
        datestart = request.form.get("datestart")
        description = request.form.get("description")
        tag = request.form.get("tag")

        # if 'present' checkbox is checked, dateend is 'Present'. If not, assign to entered value.
        if request.form.get("present"):
            dateend = "Present"
        else:
            dateend = request.form.get("dateend")
        

        # UPDATE
        if request.form['submit'] == "update":
            job_id = int(request.form.get("job_id"))
            db.execute("UPDATE employment SET user_id = ?, position = ?, company = ?, location = ?, datestart = ?, dateend = ?, description = ?, tag = ? WHERE id = ?",
                       (user_id, position, company, location, datestart, dateend, description, tag, job_id))
            db.commit()
            flash("Updated Employment History!")
            return redirect(url_for('views.employment'))

        # ADD
        if request.form['submit'] == "add":
            db.execute("INSERT INTO employment (user_id, position, company, location, datestart, dateend, description, tag) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (user_id, position, company, location, datestart, dateend, description, tag))
            db.commit()
            flash("Added to Employment History!")
            return redirect(url_for('views.employment'))
