from .models import Festival, Perfomance, Artist, Reviewer, Review
from .forms import RegistrationForm, PerfomanceSubmissionForm, ReviewForm

from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseForbidden, FileResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

def index(request):
    return render(request, 'index.html')  # Αρχική σελίδα

def festivals(request):
    festivals = Festival.objects.all()  # Φεστιβάλ από τη βάση δεδομένων
    return render(request, 'view_festivals.html', {'festivals': festivals})  # Εμφάνιση φεστιβάλ

def signup(request):
    if request.method == 'POST':  # Αν είναι POST αίτηση
        form = RegistrationForm(request.POST)
        if form.is_valid():  # Έγκυρη φόρμα
            user = form.save()  # Δημιουργία χρήστη
            login(request, user)  # Σύνδεση χρήστη
            return redirect('festivalsystem:profile')  # Ανακατεύθυνση στο προφίλ
    else:
        form = RegistrationForm()  # Δημιουργία φόρμας εγγραφής
    return render(request, 'signup.html', {'form': form})  # Εμφάνιση φόρμας εγγραφής
   

def login_view(request):
    if request.method == 'POST':  # Αν είναι POST αίτηση
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():  # Έγκυρη φόρμα σύνδεσης
            user = form.get_user()  # Λήψη χρήστη
            login(request, user)  # Σύνδεση χρήστη
            return redirect('festivalsystem:profile')  # Ανακατεύθυνση στο προφίλ
    else:
        form = AuthenticationForm() # Δημιουργία φόρμας σύνδεσης
    return render(request, 'login.html', {'form': form})  # Εμφάνιση φόρμας σύνδεσης

@login_required
def profile(request):
    user = request.user  # Λήψη δεδομένων χρήστη
    return render(request, 'profile.html', {'user': user})  # Εμφάνιση προφίλ χρήστη

@login_required
def logout_view(request):
    logout(request)  # Αποσύνδεση χρήστη
    return render(request, 'logout.html')  # Εμφάνιση σελίδας αποσύνδεσης

@login_required
def submit_perfomance(request, festival_id):
    festival = get_object_or_404(Festival, id=festival_id)  # Βρίσκουμε το φεστιβάλ
    if request.method == 'POST':  # Αν είναι POST αίτηση
        form = PerfomanceSubmissionForm(festival, request.POST, request.FILES)
        if form.is_valid():  # Έγκυρη φόρμα υποβολής
            perfomance = form.save(commit=False)  # Δημιουργία παράστασης
            perfomance.festival = festival  # Ανάθεση φεστιβάλ στην παράσταση
            perfomance.save()  # Αποθήκευση παράστασης

            artists = []  # Λίστα καλλιτεχνών

            selected_users = list(form.cleaned_data['artists'])  # Επιλεγμένοι χρήστες
            selected_users.append(request.user)  # Προσθήκη του χρήστη που υποβάλει την παράσταση
            for user in selected_users:
                artist, created = Artist.objects.get_or_create(user=user)  # Δημιουργία ή εύρεση καλλιτέχνη
                artist.festivals.add(festival)  # Προσθήκη στο φεστιβάλ
                artists.append(artist)

            perfomance.artists.set(artists)  # Ανάθεση καλλιτεχνών στην παράσταση
            perfomance.save()  # Αποθήκευση παράστασης

            return redirect('festivalsystem:perfomance_detail', perfomance_id=perfomance.id)  # Ανακατεύθυνση στις λεπτομέρειες της παράστασης
    else:
        form = PerfomanceSubmissionForm(festival)  # Δημιουργία φόρμας υποβολής παράστασης

    return render(request, 'submit_perfomance.html', {'form': form})  # Εμφάνιση φόρμας υποβολής παράστασης

@login_required
def perfomance_detail(request, perfomance_id):
    perfomance = get_object_or_404(Perfomance, id=perfomance_id)  # Βρίσκουμε την παράσταση

    if not perfomance.is_artist(request.user) and not perfomance.festival.is_organizer(request.user):
        return HttpResponseForbidden('You are not an artist.')  # Αν ο χρήστης δεν είναι καλλιτέχνης ή οργανωτής

    user_is_program_organizer = perfomance.festival.organizer_set.filter(user=request.user).exists() # Έλεγχος αν είναι οργανωτής
    user_is_reviewer = perfomance.reviewer_set.filter(user=request.user).exists()  # Έλεγχος αν είναι κριτής

    review_exists = user_is_reviewer and perfomance.review_set.filter(reviewer__user=request.user).exists()  # Έλεγχος αν υπάρχει αξιολόγηση

    context = {
        'perfomance': perfomance,
        'submissions_open': perfomance.festival.submissions_open(),  # Αν είναι ανοιχτές οι υποβολές
        'user_is_program_organizer': user_is_program_organizer,
        'user_is_reviewer': user_is_reviewer,
        'review_exists': review_exists,
    }

    return render(request, 'perfomance_detail.html', context)  # Εμφάνιση λεπτομερειών παράστασης

@login_required
def download_perfomance(request, perfomance_id):
    perfomance = get_object_or_404(Perfomance, id=perfomance_id)  # Βρίσκουμε την παράσταση

    if not request.user.is_superuser and not request.user.is_staff:
        if not perfomance.is_artist(request.user) and not perfomance.festival.is_organizer(request.user):
            return HttpResponseForbidden("Δεν έχετε επαρκή δικαιώματα για να κατεβάσετε αυτό το αρχείο")  # Αν δεν έχει δικαιώματα

    file_path = perfomance.file.path  # Παίρνουμε τη διαδρομή του αρχείου

    response = FileResponse(open(file_path, 'rb'))  # Επιστροφή του αρχείου για λήψη
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(perfomance.file.name)  # Ορισμός ονόματος αρχείου για λήψη

    return response  # Επιστροφή απάντησης

@login_required
def view_user_perfomances(request):
    user = request.user  # Λήψη χρήστη
    perfomances = Perfomance.objects.filter(artists__user=user)

    return render(request, 'view_user_perfomances.html', {'perfomances': perfomances})  # Εμφάνιση παραστάσεων χρήστη

def festival_details(request, festival_id):
    festival = Festival.objects.get(id=festival_id)
    submissions_open = festival.submissions_open()

    user_is_program_organizer = False

    if request.user.is_authenticated:
        user_is_program_organizer = festival.organizer_set.filter(user=request.user).exists()

    context = {
        'festival': festival,
        'submissions_open': submissions_open,
        'user_is_program_organizer': user_is_program_organizer,
    }

    return render(request, 'festival_details.html', context)

@login_required
def view_festival_perfomances(request, festival_id):
    festival = get_object_or_404(Festival, id=festival_id)  # Εύρεση του φεστιβάλ με το συγκεκριμένο ID

    if not festival.is_organizer(request.user):  # Έλεγχος αν ο χρήστης είναι διοργανωτής
        return HttpResponseForbidden("Απαγορεύεται η πρόσβαση.")

    tracks = festival.track_set.all()  # Εύρεση όλων των tracks του φεστιβάλ

    perfomances_by_track = {}  # Δημιουργία dictionary για κατηγοριοποίηση performances ανά track
    for track in tracks:
        perfomances_by_track[track] = festival.perfomance_set.filter(track=track)   # Ανάθεση performances σε κάθε track

    context = {
        'festival': festival,
        'perfomances_by_track': perfomances_by_track,  # Αποστολή δεδομένων στο template
    }

    return render(request, 'view_fest_perfomances.html', context)  # Προβολή template με τις πληροφορίες

@login_required
def add_reviewers(request, perfomance_id):
    perfomance = get_object_or_404(Perfomance, id=perfomance_id)  # Εύρεση του performance με το συγκεκριμένο ID

    if not perfomance.festival.is_organizer(request.user):  # Έλεγχος αν ο χρήστης είναι διοργανωτής του φεστιβάλ
        return HttpResponseForbidden("Δεν έχετε την πρόσβαση για να προσθέσετε reviewers.")  # Αν δεν είναι, απαγορεύεται

    if request.method == 'POST':   # Αν η φόρμα υποβλήθηκε
        user_id = request.POST.get('user_id')  # Λήψη του ID του χρήστη από το αίτημα
        reviewer, created = Reviewer.objects.get_or_create(user_id=user_id)  # Δημιουργία ή εύρεση του reviewer

        if perfomance not in reviewer.perfomances.all(): # Αν το performance δεν έχει ήδη reviewer
            reviewer.perfomances.add(perfomance)  # Συσχέτιση του performance με τον reviewer
        
        if perfomance.status == 'submitted':  # Αν το performance είναι σε κατάσταση "submitted"
            perfomance.status = 'under_review'  # Ενημέρωση της κατάστασης σε "under_review"
            perfomance.save()  # Αποθήκευση αλλαγών

    reviewers = perfomance.reviewer_set.all()  # Λήψη όλων των reviewers του performance
    users = User.objects.all()  # Λήψη όλων των χρηστών του συστήματος

    context = {
        'perfomance': perfomance,
        'reviewers': reviewers,
        'users': users,
    }

    return render(request, 'add_reviewers.html', context)

@login_required
def remove_reviewer(request, perfomance_id, reviewer_id):
    perfomance = get_object_or_404(Perfomance, id=perfomance_id)
    reviewer = get_object_or_404(Reviewer, id=reviewer_id)

    if not perfomance.festival.is_organizer(request.user):
        return HttpResponseForbidden("Δεν έχετε την πρόσβαση για να προσθέσετε reviewers.")

    if request.method == 'POST':  # Αν υποβλήθηκε αίτημα
        try:
            review = Review.objects.get(perfomance=perfomance, reviewer=reviewer)  # Λήψη του review αν υπάρχει
        except Review.DoesNotExist:
            review = None  # Αν δεν υπάρχει, ορίζεται ως None

        if review:
            review.delete()

        reviewer.perfomances.remove(perfomance)  # Αφαίρεση του performance από τον reviewer

    return redirect('festivalsystem:add_reviewers', perfomance_id=perfomance.id)  # Ανακατεύθυνση στη σελίδα reviewers

@login_required
def review_perfomance(request, perfomance_id):
    perfomance = get_object_or_404(Perfomance, id=perfomance_id)

    if not perfomance.is_reviewer(request.user):
        return HttpResponseForbidden("Δεν επιτρέπεται να κάνετε review αυτό το perfomance.")

    reviewer = get_object_or_404(Reviewer, user=request.user)
    review = Review.objects.filter(reviewer__user=request.user, perfomance=perfomance).first()

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = reviewer
            review.perfomance = perfomance
            review.save()
            return redirect('festivalsystem:perfomance_detail', perfomance_id=perfomance_id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'review_perfomance.html', {'form': form, 'perfomance': perfomance})
