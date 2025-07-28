from django.shortcuts import render, redirect
import asyncio
from django.http import FileResponse, Http404
from django.conf import settings
from pathlib import Path
from playwright.async_api import async_playwright
from .models import Profile
# Create your views here.

def accept(request):

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        summary = request.POST.get("summary")
        degree = request.POST.get("degree")
        school = request.POST.get("school")
        university = request.POST.get("university")
        previous_work = request.POST.get("previous_work")
        skills = request.POST.get("skills")

        profile = Profile(
            name=name,
            email=email,
            phone=phone,
            summary=summary,
            degree=degree,
            school=school,
            university=university,
            previous_work=previous_work,
            skills=skills
        )
        profile.save()
        return redirect('user_list')


    return render(request, 'pdf/accept.html')

def resume(request, id):
    user_profile = Profile.objects.get(pk=id)
    return render(request,'pdf/resume.html', {'user_profile': user_profile})

async def generate_pdf(url: str, output_path: Path):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.pdf(path=str(output_path), format='A4')
        await browser.close()

def resume_pdf(request, id):
    try:
        profile = Profile.objects.get(pk=id)
    except Profile.DoesNotExist:
        raise Http404("Profile not found")

    # URL for the HTML resume page (make sure your server is running)
    url = request.build_absolute_uri(f'/{id}/')

    output_dir = Path(settings.BASE_DIR) / "pdfs"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f'resume_{id}.pdf'

    # Run the async playwright task synchronously
    asyncio.run(generate_pdf(url, output_file))

    # Serve the generated PDF file
    return FileResponse(open(output_file, 'rb'), content_type='application/pdf')

def user_list(request):
    users = Profile.objects.all()
    return render(request, 'pdf/user_list.html', {'users': users})