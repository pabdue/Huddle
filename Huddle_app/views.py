from django.shortcuts import render, redirect, get_object_or_404
from .models import Account
from django.contrib import messages
from .models import Account, HuddleGroup, Task, HuddleGroupMembers
from django.http import JsonResponse
from django.db import transaction

def huddle_home(request):
    # Get user information from the session
    user_id = request.session.get('user_id')
    username = request.session.get('username')

    if not user_id or not username:
        # If user information is not in the session, redirect to login
        return redirect('Huddle_app:huddle_login')

    try:
        # Get the user's account
        account = Account.objects.get(id=user_id, username=username)

        # Get the user's huddle groups
        huddle_groups = HuddleGroup.objects.filter(members=account)

        return render(request, 'index.html', {'account': account, 'huddle_groups': huddle_groups})
    except Account.DoesNotExist:
        # If the user does not exist, display an error message
        messages.error(request, "User not found.")
        return redirect('Huddle_app:huddle_login')

def create_huddle(request):
    if request.method == 'POST':
        # Assuming you have a form with 'huddleName' and 'members' fields
        huddle_name = request.POST.get('huddleName')
        members_emails = request.POST.get('members')

        # Get user information from the session
        user_id = request.session.get('user_id')
        username = request.session.get('username')

        

        if not user_id or not username:
            # If user information is not in the session, redirect to login
            return JsonResponse({'success': False, 'error': 'User not authenticated.'})

        # Get the user's account
        account = Account.objects.get(username=username)
        members_emails = members_emails + ', ' + account.email
        # Create a new HuddleGroup instance and save it to the database
        huddle_group = HuddleGroup.objects.create(
            name=huddle_name,
        )
        # Use set() to add members to the many-to-many relationship
        huddle_group.members.set(Account.objects.filter(email__in=members_emails.replace(' ', '').split(',')))

        # Fetch the user's huddle groups
        huddle_groups = HuddleGroup.objects.filter(members=account)

        # Pass the user's huddle groups to the template
        return redirect('Huddle_app:huddle_home')

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def huddle_group(request, huddle_group_id):
    # Get user information from the session
    user_id = request.session.get('user_id')
    username = request.session.get('username')

    if not user_id or not username:
        # If user information is not in the session, redirect to login
        return redirect('Huddle_app:huddle_login')

    try:
        # Get the user's huddle groups
        user = Account.objects.get(id=user_id, username=username)
        
        # Check if the user is a member of the requested huddle group
        huddle_group = get_object_or_404(HuddleGroup, id=huddle_group_id)

        # Get all members associated with the huddle group
        members = HuddleGroupMembers.objects.filter(huddlegroup=huddle_group).select_related('account')
        other_members = huddle_group.members.all()

        tasks = Task.objects.filter(huddle_group=huddle_group)

        context = {
            'huddle_group': huddle_group,
            'members': members,
            'other_members': other_members,
            'tasks': tasks,
            # Include other context variables as needed
        }

        return render(request, 'huddle_page.html', context)
    except Account.DoesNotExist:
        # If the user does not exist, display an error message
        messages.error(request, "User not found.")
        return redirect('Huddle_app:huddle_login')
    
@transaction.atomic
def create_task(request, huddle_group_id):
    if request.method == 'POST':
        # Assuming you have the necessary form fields in the request
        task_name = request.POST.get('taskName')
        task_description = request.POST.get('taskDescription')
        assigned_members = request.POST.get('assignedMembers')
        due_date = request.POST.get('dueDate')

        # Get user information from the session
        user_id = request.session.get('user_id')
        username = request.session.get('username')

        if not user_id or not username:
            # If user information is not in the session, redirect to login
            return JsonResponse({'success': False, 'error': 'User not authenticated.'})

        try:
            # Get the user's account
            account = Account.objects.get(id=user_id, username=username)

            # Get the huddle group using the ID from the URL parameters
            try:
                huddle_group = HuddleGroup.objects.get(id=huddle_group_id)
            except HuddleGroup.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'HuddleGroup not found.'})

            try:
                # Create a new task instance and save it to the database
                task = Task.objects.create(
                    name=task_name,
                    description=task_description,
                    people_assigned=assigned_members,
                    deadline=due_date,
                    huddle_group=huddle_group  # Associate the task with the huddle group
                )
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})

            # Redirect to the huddle_group view with the appropriate huddle_group_id
            return redirect('Huddle_app:huddle_group', huddle_group_id=huddle_group.id)

        except Account.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def huddle_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Try to get the user from the database
            user = Account.objects.get(username=username)
            
            # Check if the provided password matches
            if password == user.password:
                # Set user information in the session
                request.session['user_id'] = user.id
                request.session['username'] = user.username

                return redirect('Huddle_app:huddle_home')  # Redirect to the home page after login
            else:
                # If the password is not valid, display an error message
                messages.error(request, "Invalid username or password.")
                return redirect('Huddle_app:huddle_login')
        except Account.DoesNotExist:
            # If the user does not exist, display an error message
            messages.error(request, "Invalid username or password.")
            return redirect('Huddle_app:huddle_login')

    return render(request, 'login.html')

def huddle_signup(request):
    if request.method == 'POST':
        # Extract data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Perform basic form validation
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('Huddle_app:huddle_signup')

        # Check if the username or email is already taken
        if Account.objects.filter(username=username).exists() or Account.objects.filter(email=email).exists():
            messages.error(request, "Username or email already taken.")
            return redirect('Huddle_app:huddle_signup')

        # Create an Account instance and save it to the database
        account = Account(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password1
        )
        account.save()

        # Optionally, you might want to log in the user after signing up
        # For simplicity, we'll redirect to the login page
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('Huddle_app:huddle_login')

    return render(request, 'signup.html')

@transaction.atomic
def add_member(request, huddle_group_id):
    if request.method == 'POST':
        # Assuming you have the necessary form fields in the request
        member_email = request.POST.get('memberEmail')

        # Get user information from the session
        user_id = request.session.get('user_id')
        username = request.session.get('username')

        if not user_id or not username:
            # If user information is not in the session, redirect to login
            return JsonResponse({'success': False, 'error': 'User not authenticated.'})

        try:
            # Get the huddle group using the ID from the URL parameters
            huddle_group = HuddleGroup.objects.get(id=huddle_group_id)

            # Get the account based on the provided email
            account = Account.objects.get(email=member_email)

            # Check if the user is already a member of the huddle group
            if HuddleGroupMembers.objects.filter(huddlegroup=huddle_group, account=account).exists():
                return JsonResponse({'success': False, 'error': 'User is already a member.'})

            # Create a new entry in the HuddleGroupMembers table
            HuddleGroupMembers.objects.create(huddlegroup=huddle_group, account=account)

            return redirect('Huddle_app:huddle_group', huddle_group_id=huddle_group.id)

        except Account.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found.'})
        except HuddleGroup.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'HuddleGroup not found.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})
