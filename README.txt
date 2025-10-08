
Task Manager - Django Project

Overview: 
This project is a Django-based web application that helps manage tasks, bug reports, and notes.
(I decided to add more model to be able to implement them with inheritence)
It includes both a web interface and API endpoints for CRUD operations (Create, Read, Update, Delete).

The goal was to make a simple but organized system where users can create and track their work.
I also tried to keep the code clean and reusable by using base classes and mixins.

Main Features

- Login system (only logged-in users can create or edit items)
- CRUD pages for Tasks, Bug Reports, and Notes
- Search bar for all pages
- Log system that records all actions (create, update, delete, search)
- REST API endpoints for all models
- Uses SQLite as the database
- Testing views

Design Decisions 

1. Base Views:
   I made base views for both UI and API to avoid repeating code. 
   For example, all list views inherit from one base class that handles search and filtering.

2. Logging:
   I added logging to track user activity. Each action like creating or deleting something is saved in a log file.
   Example: "User 'mahta' created Task titled 'Fix homepage UI'"

3. Search Feature:
   I added a search box to help users find their tasks, notes, or bug reports easily(based on the project description it search by title and description and the result shows item's detail ).

4. API Endpoints:
   I used Django REST Framework to create API endpoints for all three models. 
   Each model has two main endpoints: one for list/create and one for detail/update/delete.
5. Using Generic Views
Since in this project I was focusing on CRUD oprations, generic class_bassed_view helps me handle the operation automatically, so instead of writing repetitive code for listing, creating, editing or deleting objects I have used ListView, DetailView, CreateView, UpdateView, DeleteView

6. Login System
By using LoginREquiredMixin and UserPassesTestMixin, it ensures that logged in user can create ,edit,or delete.


Models

- BaseItem: title, description, owner, created_at, update_at
- Task:(BaseItem's fields), status, priority, assigned_to
- BugReport: (BaseItem's fields), severity, status, expected_result
- Note: (BaseItem's fields), note_type, is_pinned, tags

All models have an “owner” field so users only see and edit their own data.

API Routes

- /api/tasks/ → list and create tasks
- /api/tasks/<id>/ → view, edit, delete task
- /api/bugs/ → list and create bug reports
- /api/bugs/<id>/ → view, edit, delete bug report
- /api/notes/ → list and create notes
- /api/notes/<id>/ → view, edit, delete note

Or you can also search using ?q= in the URL, for example:
  /api/tasks/?q=design


View Tests:
- Tested home, list, detail, create, update, and delete views.
- Checked authentication (redirects for unauthenticated users).
- Only the creator can edit or delete.



Conclusion
This project helped me learn how to organize Django views, work with APIs, and deploy a full project online.

