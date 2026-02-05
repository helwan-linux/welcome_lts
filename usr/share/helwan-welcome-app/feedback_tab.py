from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QTextEdit, QPushButton,
    QLabel, QHBoxLayout, QMessageBox, QComboBox, QCheckBox,
    QListWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication
import webbrowser
from urllib.parse import quote_plus

# ====== Session-only storage (RAM) ======
SESSION_FEEDBACK = []

def create_feedback_tab(parent, _):
    tab = QWidget()
    layout = QVBoxLayout(tab)
    layout.setAlignment(Qt.AlignTop)

    # =========================
    # Rating
    # =========================
    rating_group = QGroupBox(_("Rate Your Experience"))
    rating_layout = QHBoxLayout()
    rating_label = QLabel(_("Select rating:"))
    rating_combo = QComboBox()
    rating_combo.addItems(["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"])
    rating_layout.addWidget(rating_label)
    rating_layout.addWidget(rating_combo)
    rating_group.setLayout(rating_layout)
    layout.addWidget(rating_group)

    # =========================
    # Comments
    # =========================
    comments_group = QGroupBox(_("Suggestions / Comments"))
    comments_layout = QVBoxLayout()
    comments_text = QTextEdit()
    comments_text.setPlaceholderText(
        _("Write your feedback here. No account required.")
    )
    comments_layout.addWidget(comments_text)
    comments_group.setLayout(comments_layout)
    layout.addWidget(comments_group)

    # =========================
    # Send Options
    # =========================
    send_group = QGroupBox(_("Send Options"))
    send_layout = QVBoxLayout()

    chk_github = QCheckBox(_("Open GitHub Issue"))
    chk_email = QCheckBox(_("Send via Email"))
    chk_copy = QCheckBox(_("Copy feedback to clipboard"))

    send_layout.addWidget(chk_github)
    send_layout.addWidget(chk_email)
    send_layout.addWidget(chk_copy)

    send_group.setLayout(send_layout)
    layout.addWidget(send_group)

    # =========================
    # Statistics (Session only)
    # =========================
    stats_group = QGroupBox(_("Session Statistics"))
    stats_layout = QVBoxLayout()

    lbl_total = QLabel(_("Feedbacks this session: 0"))
    lbl_avg = QLabel(_("Average Rating: 0 ⭐"))

    lst_recent = QListWidget()
    lst_recent.setFixedHeight(100)

    stats_layout.addWidget(lbl_total)
    stats_layout.addWidget(lbl_avg)
    stats_layout.addWidget(QLabel(_("Last comments:")))
    stats_layout.addWidget(lst_recent)

    stats_group.setLayout(stats_layout)
    layout.addWidget(stats_group)

    # =========================
    # Submit Button
    # =========================
    btn_submit = QPushButton(_("Submit Feedback"))
    layout.addWidget(btn_submit)

    # =========================
    # Helpers
    # =========================
    def update_statistics():
        total = len(SESSION_FEEDBACK)
        lbl_total.setText(_("Feedbacks this session: ") + str(total))

        if total:
            stars = [len(f["rating"]) for f in SESSION_FEEDBACK]
            avg = sum(stars) / total
            lbl_avg.setText(_("Average Rating: ") + f"{avg:.2f} ⭐")

            lst_recent.clear()
            for f in SESSION_FEEDBACK[-5:]:
                if f["comments"]:
                    lst_recent.addItem(f["comments"])
        else:
            lbl_avg.setText(_("Average Rating: 0 ⭐"))
            lst_recent.clear()

    def submit_feedback():
        rating = rating_combo.currentText()
        comments = comments_text.toPlainText().strip()

        if not comments:
            QMessageBox.warning(
                parent,
                _("Empty feedback"),
                _("Please write a comment before submitting.")
            )
            return

        feedback_text = f"Rating: {rating}\n\n{comments}"

        # Save in RAM only
        SESSION_FEEDBACK.append({
            "rating": rating,
            "comments": comments
        })
        update_statistics()

        # =========================
        # إرسال اختياري
        # =========================
        if chk_github.isChecked():
            title = quote_plus(f"Feedback: {rating}")
            body = quote_plus(comments)
            url = (
                "https://github.com/helwan-linux/helwan-feedback/"
                f"issues/new?title={title}&body={body}"
            )
            webbrowser.open(url)

        if chk_email.isChecked():
            subject = quote_plus(f"Helwan Linux Feedback {rating}")
            body = quote_plus(comments)
            mailto = f"mailto:helwanlinux@gmail.com?subject={subject}&body={body}"
            webbrowser.open(mailto)

        if chk_copy.isChecked():
            QGuiApplication.clipboard().setText(feedback_text)

        QMessageBox.information(
            parent,
            _("Thank you"),
            _("Feedback handled successfully.")
        )

        comments_text.clear()
        rating_combo.setCurrentIndex(0)
        chk_github.setChecked(False)
        chk_email.setChecked(False)
        chk_copy.setChecked(False)

    btn_submit.clicked.connect(submit_feedback)
    layout.addStretch(1)

    return tab
