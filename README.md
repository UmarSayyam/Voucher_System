# Vouchers System

This is a Django-based voucher management system designed for managing and assigning vouchers to bakery members. It supports many-to-many relationships between members and vouchers, along with real-time WebSocket notifications for voucher usage.

## Features

- Voucher creation, updating, and deletion.
- Assign vouchers to members and track usage.
- Real-time notifications when a voucher is used or expires.
- JWT token-based authentication for secure API access.
- Special conditions like birthday-only vouchers.

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Real-Time**: Django Channels, WebSockets
- **Authentication**: JWT (JSON Web Token)
- **Database**: SQLite, Postgres
 
## Installation

### Prerequisites

- Python 3.x
- Django
- Django Channels
- Postman or a WebSocket client for testing.

### Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/vouchers-system.git    # i will add link after completion
