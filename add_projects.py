import datetime
from peewee import DoesNotExist, InternalError
from app.models import Project, db
from slugify import slugify

# Moved create_tables() to be safely handled
def ensure_tables():
    try:
        # Import but don't run create_tables directly
        from app.models import create_tables
        with db.atomic() as transaction:
            try:
                create_tables()
            except InternalError as e:
                # Handle the specific transaction aborted error
                transaction.rollback()
                print(f"Transaction error during table creation: {e}")
                # Try to recover by explicitly closing the connection
                db.close()
                db.connect()
            except Exception as e:
                transaction.rollback()
                print(f"Error creating tables: {e}")
                raise
    except Exception as e:
        print(f"Database setup error: {e}")
        
# Call our safer function
ensure_tables()

# --- New Project Data ---
# Rest of your code remains the same...
new_projects_data = [
    {
        "title": "Core DB",
        "description": "Bu layihə istifadəçilərə ağıllı axtarış, çoxlu filtrasiya, vizualizasiya və Spotfire və Power BI kimi sənaye proqram təminatları ilə inteqrasiya kimi funksionallıqları özündə birləşdirən məlumatların təhlili üçün hərtərəfli və normallaşdırılmış verilənlər bazası təqdim etməyi hədəfləyir.\n\nBu layihənin bir hissəsi olaraq, istifadəçilərə 20 ili əhatə edən 10,000-dən çox fayldan ibarət böyük arxivdən lazımi hesabat fayllarını tez bir zamanda axtarmağa və yükləməyə imkan verən Hesabatlar səhifəsi hazırladım. Həmçinin, genişləndirilmiş funksionallıq üçün Azure Full-Text Search və əlavə wildcardlar istifadə edərək axtarış mühərriki tətbiq etdim.\n\nƏlavə olaraq, şəkil PDF fayllarını mətn formatına çevirmək üçün Optik Simvol Tanıma (OCR) istifadə edən bir alqoritm, həmçinin rəqəmsal cədvəl məlumatlarını lasio fayl formatına çevirmək üçün başqa bir alqoritm yaratdım. Həmçinin 1500-dən çox rəqəmsal məlumat vərəqi faylını təhlil etdim, yenidən formalaşdırdım və təmizlədim.\n\nMən həmçinin Hesabatlar səhifəsi üçün admin səhifəsinin və layihədəki digər səhifələr üçün əlavə funksiyaların hazırlanması üzərində işləmişəm. Ümumilikdə, bu layihə mənə məlumatların təhlili və verilənlər bazasının idarə edilməsi sahəsində dəyərli təcrübə qazandırıb.",
        "short_description": "Ağıllı axtarış, filtrasiya, vizualizasiya və inteqrasiya imkanları ilə məlumatların təhlili üçün hərtərəfli və normallaşdırılmış verilənlər bazası.",
        "client": "Digital Research Lab", # Associated with
        "completion_date": datetime.date(2022, 1, 31), # Assuming end of Jan 2022
        "technologies_used": "Azure Full-Text Search, OCR, Python, Palantir (implied), Spotfire (integration), Power BI (integration)", # Extracted/Inferred
        "featured": False, # Set to True if you want it on the homepage
        "category_id": 1 # Data Analysis & Search
    },
    {
        "title": "Slug Detection",
        "description": "Layihə çərçivəsində neft və qaz quyularının real vaxt rejimində monitorinqi üçün mürəkkəb riyazi lüb aşkarlama alqoritmi hazırladım. Layihə Palantir platformasına əsaslanırdı və quyularda mümkün problemləri aşkar etmək və mühəndislərə bildirmək üçün bir alqoritmin yaradılmasını əhatə edirdi.\n\nAlqoritmin dəqiqliyini təmin etmək üçün 200-dən çox quyudan gələn səs-küylü məlumatları yenidən formalaşdırdım və təmizlədim və alqoritmi bütün quyuların məlumatlarına tətbiq etdim. Layihənin yekun nəticəsi məlumat nəticələrini asanlıqla təhlil etmək və şərh etmək üçün bir idarəetmə paneli oldu.\n\nBu layihə vasitəsilə məlumatların təhlili və alqoritm hazırlanması sahəsində dəyərli təcrübə qazandım və bu sahələrdə öyrənməyə və böyüməyə davam etməkdən məmnunam.",
        "short_description": "Palantir platformasından istifadə edərək neft və qaz quyularının real vaxt rejimində monitorinqi üçün mürəkkəb riyazi lüb aşkarlama alqoritmi.",
        "client": "Digital Research Lab", # Associated with
        "completion_date": datetime.date(2021, 6, 30), # Assuming end of Jun 2021
        "technologies_used": "Python, Palantir, Data Analysis, Algorithm Development", # Extracted/Inferred
        "featured": False,
        "category_id": 2 # Real-Time Monitoring & Algorithm
    },
    {
        "title": "AlienBlog",
        "description": "AlienBlog sadəlik və sürət üçün nəzərdə tutulmuş minimalist bir bloq platformasıdır. Təmiz interfeysi və sadə nəşr iş axını ilə seçilir, bu da onu diqqəti yayındırmayan bloq təcrübəsi axtaran tərtibatçılar və ya yazıçılar üçün ideal edir.",
        "short_description": "Sadəlik və sürət üçün nəzərdə tutulmuş minimalist bloq platforması.",
        "technologies_used": "Naməlum (Veb Texnologiyaları güman edilir)", # Not specified
        "featured": False,
        "category_id": 3 # Blog Platforms
    },
    {
        "title": "Albom",
        "description": "Albom fotoşəkil kolleksiyasını idarə etmək və göstərmək üçün Django əsaslı veb tətbiqidir. İstifadəçilər fotoşəkillər qalereyasına baxa, fərdi fotoşəkilləri təsvirləri ilə birlikdə ətraflı görə və təsvirləri ilə yeni fotoşəkillər əlavə edə bilərlər.\n\nƏsas Xüsusiyyətlər:\nFoto Qalereyası: Kolleksiyadakı bütün fotoşəkilləri göstərir.\nFoto Detalları: Fərdi fotoşəkilləri təsvirləri ilə birlikdə göstərir.\nYeni Foto Əlavə Et: İstifadəçilərə yeni fotoşəkillər yükləməyə və təsvirlər təqdim etməyə imkan verir.",
        "short_description": "Fotoşəkil kolleksiyasını idarə etmək və göstərmək üçün Django əsaslı veb tətbiqi.",
        "technologies_used": "Python, Django",
        "featured": False,
        "category_id": 4 # Photo Gallery Applications
    },
    {
        "title": "140-Vibes",
        "description": "140 Vibes, 140 Vibes hip-hop qrupunun musiqi, albom, profil və məhsullarını nümayiş etdirmək və idarə etmək üçün nəzərdə tutulmuş hərtərəfli veb platformadır. Trek, albom, məhsul və profillərə baxmaq, həmçinin YouTube video baxışları və bəyənmələri üçün ətraflı statistika daxil olmaqla müxtəlif funksionallıqlara malikdir.\n\nƏsas Xüsusiyyətlər:\nAna Səhifə: Albomların siyahısını göstərir.\nTreklər Səhifəsi: Bütün trekləri yaradılma tarixinə görə sıralayır.\nAlbomlar Səhifəsi: Bütün albomları yaradılma tarixinə görə sıralayır.\nTrack Detal Səhifəsi: YouTube statistikası daxil olmaqla, müəyyən bir trek haqqında ətraflı məlumat göstərir.\nAlbom Detal Səhifəsi: Trek detalları və ümumiləşdirilmiş YouTube statistikası ilə birlikdə müəyyən bir albomun detallarını göstərir.\nMağaza Səhifəsi: Şəkilləri daxil olmaqla, satın alına bilən bütün məhsulları sıralayır.\nMəhsul Detal Səhifəsi: Bütün əlaqəli şəkillər daxil olmaqla, müəyyən bir məhsul haqqında ətraflı məlumat göstərir.\nProfil Səhifəsi: Hip-hop qrupu üzvləri haqqında məlumat göstərir.",
        "short_description": "140 Vibes hip-hop qrupu üçün musiqi, albom, profil və məhsulları nümayiş etdirmək və idarə etmək üçün veb platforma.",
        "technologies_used": "Python, Django",
        "featured": False,
        "category_id": 5 # Music & Media Platforms
    },
    {
        "title": "Weather-Information-App",
        "description": "Hava Məlumatı Tətbiqi, Weatherstack API istifadə edərək Azərbaycandakı müxtəlif şəhərlər üçün cari hava məlumatlarını əldə edən və göstərən Tkinter ilə qurulmuş bir masaüstü tətbiqidir. Hava məlumatları cədvəl formatında təqdim olunur və tətbiq həmçinin məlumatları CSV faylına saxlayır.\n\nƏsas Xüsusiyyətlər:\nHava Məlumatlarının Alınması: Bir çox şəhər üçün cari hava məlumatlarını əldə edir.\nMəlumatların Göstərilməsi: Hava məlumatlarını Tkinter cədvəlində göstərir.\nMəlumatların İxracı: Hava məlumatlarını CSV faylına saxlayır.",
        "short_description": "Weatherstack API-dən Azərbaycan hava məlumatlarını əldə edən və göstərən Tkinter masaüstü tətbiqi.",
        "technologies_used": "Python, Tkinter, Requests, Pandas",
        "featured": False,
        "category_id": 6 # Weather Applications
    },
    {
        "title": "Internet-Club-Sale-Management",
        "description": "İnternet Klub Qiymət Kalkulyatoru, istifadəçilərə sərf olunan vaxta əsasən müxtəlif otaqların (standart otaq və ya kabinet) istifadə dəyərini müəyyənləşdirməyə kömək edən veb əsaslı bir tətbiqdir. İstifadəçilər müddəti və ümumi dəyəri hesablamaq üçün başlanğıc və bitmə vaxtlarını daxil edə bilərlər. Tətbiq responsiv dizayna malikdir və HTML5, CSS3, JavaScript (jQuery), Bootstrap 4.3.1 və FontAwesome istifadə edilərək qurulmuşdur.\n\nƏsas Xüsusiyyətlər:\nOtaq Seçimi: İstifadəçilər standart otaq və ya kabinet arasında seçim edə bilərlər.\nVaxt Daxiletmə: İstifadəçilər müddəti hesablamaq üçün başlanğıc və bitmə vaxtlarını daxil edə bilərlər.\nQiymət Hesablanması: Tətbiq sərf olunan vaxta və otaq tipinə əsasən ümumi dəyəri hesablayır.\nResponsiv Dizayn: Planşet müxtəlif ekran ölçülərində yaxşı işləyir.",
        "short_description": "Sərf olunan vaxta və otaq tipinə əsaslanan veb əsaslı internet klub qiymət kalkulyatoru.",
        "technologies_used": "HTML5, CSS3, JavaScript, jQuery, Bootstrap 4.3.1, FontAwesome",
        "featured": False,
        "category_id": 7 # Sales & Time Management
    }
]
# --- Function to Add Projects ---
def add_projects():
    added_count = 0
    skipped_count = 0

    # Make sure we have a fresh connection
    if db.is_closed():
        db.connect()

    try: # Outer try for the whole process
        with db.atomic() as transaction: # Use a transaction
            for data in new_projects_data:
                project_slug = slugify(data['title'])
                try:
                    # Check if project with the same slug already exists
                    Project.get(Project.slug == project_slug)
                    print(f"Skipping: Project '{data['title']}' (slug: {project_slug}) already exists.")
                    skipped_count += 1
                except DoesNotExist:
                    # Project does not exist, create it
                    try:
                        Project.create(
                            title=data['title'],
                            slug=project_slug,
                            description=data.get('description', ''),
                            short_description=data.get('short_description', ''),
                            thumbnail=data.get('thumbnail'), # Add path like 'images/projects/core_db_thumb.jpg' later
                            featured=data.get('featured', False),
                            client=data.get('client'),
                            completion_date=data.get('completion_date'),
                            technologies_used=data.get('technologies_used'),
                            project_url=data.get('project_url'),
                            category_id=data.get('category_id') # Assign category_id
                        )
                        print(f"Added: Project '{data['title']}'")
                        added_count += 1
                    except Exception as e:
                        # Log error for specific project creation but continue
                        print(f"Error adding project '{data['title']}': {e}")
                        # Optionally rollback the inner transaction if needed,
                        # but atomic() usually handles this for the whole block.
                        # If one project fails, the whole transaction might roll back
                        # depending on DB and Peewee settings.
                        # For robustness, could handle errors more granularly.

    except Exception as e:
        # Catch broader errors like connection issues or transaction failures
        print(f"An overall error occurred during the add_projects process: {e}")
        # Ensure transaction is rolled back if it was started and failed
        # Peewee's atomic() context manager should handle this, but explicit rollback can be added if needed.
        # try:
        #     transaction.rollback()
        # except NameError: # If transaction wasn't successfully initiated
        #     pass
        # except Exception as rb_err:
        #     print(f"Error during rollback: {rb_err}")

    finally:
        # Always try to close the connection
        if not db.is_closed():
            db.close()

    print(f"\nFinished adding projects.")
    print(f"Added: {added_count}")
    print(f"Skipped (already exist): {skipped_count}")


# --- Run the function ---
if __name__ == "__main__":
    add_projects()
