from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils import timezone
from .models import Ticket, Technician

@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})

@login_required
@permission_required('tickets.can_mark_completed', raise_exception=True)
def mark_completed(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    if request.user != ticket.technician.user:
        messages.error(request, "You can only mark your own tickets as completed.")
        return redirect('ticket_list')
    
    ticket.work_status = "Completed"
    ticket.approval_status = "Pending Review"
    ticket.completed_at = timezone.now()
    ticket.save()
    messages.success(request, "Ticket marked as completed! Awaiting supervisor approval.")
    return redirect('ticket_detail', ticket_id=ticket_id)

@login_required
@permission_required('tickets.can_approve', raise_exception=True)
def approve_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    if request.user == ticket.technician.user:
        messages.error(request, "You cannot approve your own work.")
        return redirect('ticket_list')
    
    action = request.POST.get('action')
    if action == "approve":
        ticket.approval_status = "Approved"
        ticket.approved_by = request.user
        ticket.approved_at = timezone.now()
    elif action == "reject":
        ticket.approval_status = "Rejected"
        ticket.work_status = "In Progress"
    
    ticket.save()
    messages.success(request, f"Ticket {action}ed.")
    return redirect('ticket_list')
