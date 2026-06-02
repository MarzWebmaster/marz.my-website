#!/usr/bin/env python3
"""Apply SEO schemas and content expansions to all marz.my pages"""
import re, json

# ============================================================
# SCHEMAS
# ============================================================

ORGANIZATION_SCHEMA = '''    <!-- Organization Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Organization",
      "@id": "https://marz.my/#organization",
      "name": "Marz Technology & Trading",
      "legalName": "Marz Technology & Trading",
      "url": "https://marz.my/",
      "logo": "https://marz.my/logo.png",
      "description": "Enterprise IT infrastructure, AI agents, cybersecurity, and digital transformation solutions for Malaysian businesses since 2004.",
      "foundingDate": "2004",
      "founder": {
        "@type": "Person",
        "name": "Remy"
      },
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "No. 7A, Jalan Orkid 1, Seksyen BS1, Bandar Saujana Utama",
        "addressLocality": "Puncak Alam",
        "addressRegion": "Selangor",
        "postalCode": "42300",
        "addressCountry": "MY"
      },
      "contactPoint": [
        {
          "@type": "ContactPoint",
          "telephone": "+60-13-361-1046",
          "contactType": "sales",
          "areaServed": "MY",
          "availableLanguage": ["English", "Malay"]
        },
        {
          "@type": "ContactPoint",
          "telephone": "+60-13-361-1046",
          "contactType": "customer support",
          "areaServed": "MY",
          "availableLanguage": ["English", "Malay"]
        }
      ],
      "sameAs": [
        "https://www.facebook.com/marztechnology",
        "https://www.linkedin.com/company/marz-technology",
        "https://www.instagram.com/marztechnology"
      ],
      "areaServed": {
        "@type": "Country",
        "name": "Malaysia"
      },
      "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "IT Services",
        "itemListElement": [
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "IT Infrastructure & Support"}},
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Networking Solutions"}},
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "AI & Intelligent Automation"}},
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "CCTV & Security Systems"}},
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Web & System Development"}},
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Cloud Solutions"}},
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Cybersecurity Audit"}},
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "IT Consultancy"}}
        ]
      },
      "taxID": "001884868V",
      "vatID": "001884868V",
      "slogan": "Future-Ready Technology Solutions for Your Business"
    }
    </script>'''

LOCALBUSINESS_SCHEMA = '''    <!-- LocalBusiness Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "@id": "https://marz.my/#localbusiness",
      "name": "Marz Technology & Trading",
      "image": "https://marz.my/logo.png",
      "url": "https://marz.my/",
      "telephone": "+60-13-361-1046",
      "priceRange": "RM50 - RM50000",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "No. 7A, Jalan Orkid 1, Seksyen BS1, Bandar Saujana Utama",
        "addressLocality": "Puncak Alam",
        "addressRegion": "Selangor",
        "postalCode": "42300",
        "addressCountry": "MY"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": "3.2345",
        "longitude": "101.4230"
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
          "opens": "09:00",
          "closes": "18:00"
        },
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": "Saturday",
          "opens": "09:00",
          "closes": "13:00"
        }
      ],
      "areaServed": [
        {"@type": "City", "name": "Kuala Lumpur"},
        {"@type": "City", "name": "Shah Alam"},
        {"@type": "City", "name": "Petaling Jaya"},
        {"@type": "City", "name": "Klang"},
        {"@type": "City", "name": "Puncak Alam"},
        {"@type": "State", "name": "Selangor"},
        {"@type": "Country", "name": "Malaysia"}
      ],
      "hasMap": "https://maps.google.com/?q=Marz+Technology+Puncak+Alam",
      "parentOrganization": {"@id": "https://marz.my/#organization"}
    }
    </script>'''

def get_breadcrumb_schema(items):
    """Generate BreadcrumbList schema from list of (name, url) tuples"""
    item_list = []
    for i, (name, url) in enumerate(items, 1):
        item_list.append({
            "@type": "ListItem",
            "position": i,
            "name": name,
            "item": url
        })
    return f'''    <!-- BreadcrumbList Schema -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": {json.dumps(item_list, indent=6)}
    }}
    </script>'''

FAQ_SERVICES_SCHEMA = '''    <!-- FAQ Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What IT services does Marz Technology offer in Malaysia?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Marz Technology offers 12 core IT services: IT infrastructure & support, networking solutions, CCTV & security systems, web development, system development, cloud solutions, IT consultancy, data recovery, IT products & peripherals, computer rental, cybersecurity audit, and IT support packages. All services are available across Malaysia."
          }
        },
        {
          "@type": "Question",
          "name": "How much do IT support services cost?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Our IT support packages start from RM200/month for basic support. We also offer customized solutions based on your business size and requirements. Contact us for a free consultation and quote tailored to your needs."
          }
        },
        {
          "@type": "Question",
          "name": "Do you serve government and enterprise clients?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes. With over 20 years of experience since 2004, we have served Malaysian government agencies, enterprises, and SMEs. We comply with government procurement standards and are experienced in tender processes."
          }
        },
        {
          "@type": "Question",
          "name": "Where is Marz Technology located?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Our office is located at No. 7A, Jalan Orkid 1, Seksyen BS1, Bandar Saujana Utama, 42300 Puncak Alam, Selangor. We serve clients throughout Klang Valley and nationwide."
          }
        }
      ]
    }
    </script>'''

FAQ_AI_SCHEMA = '''    <!-- FAQ Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What AI solutions does Marz Technology provide?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "We provide end-to-end AI solutions including AI chatbots & virtual assistants, intelligent process automation, AI data analytics & business intelligence, custom AI agent development, natural language processing (NLP), and computer vision. All solutions are tailored for Malaysian businesses."
          }
        },
        {
          "@type": "Question",
          "name": "How can AI help my business in Malaysia?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "AI can automate customer service (24/7 chatbots), streamline operations (document processing, data entry), generate business insights (predictive analytics), enhance marketing (personalized campaigns), and reduce operational costs by 30-60%. We build custom AI agents that integrate with WhatsApp, Telegram, and your existing systems."
          }
        },
        {
          "@type": "Question",
          "name": "How much does an AI chatbot or AI agent cost?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Our AI solutions start from RM1,000/month for basic AI chatbots. Custom AI agent development starts from RM5,000 depending on complexity. We offer free consultation to assess your needs and provide an accurate quote."
          }
        },
        {
          "@type": "Question",
          "name": "Can AI agents integrate with WhatsApp and other platforms?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes. Our AI agents integrate seamlessly with WhatsApp, Telegram, Facebook Messenger, email, and your website. They can also connect to your CRM, ERP, and database systems for full workflow automation."
          }
        }
      ]
    }
    </script>'''

# ============================================================
# CONTENT EXPANSIONS
# ============================================================

PRODUCTS_EXTRA_CONTENT = '''
        <!-- Expanded Product Categories -->
        <section class="product-detail">
            <h2>Why Choose Marz Technology for IT Products?</h2>
            <div class="benefits-grid">
                <div class="benefit-card">
                    <h3>Genuine Products, Guaranteed</h3>
                    <p>All products sourced from authorized distributors with full manufacturer warranty. We never sell counterfeit or refurbished items as new.</p>
                </div>
                <div class="benefit-card">
                    <h3>Competitive Pricing</h3>
                    <p>Leveraging 20+ years of supplier relationships to offer you the best prices on computers, servers, and networking equipment in Malaysia.</p>
                </div>
                <div class="benefit-card">
                    <h3>Nationwide Delivery</h3>
                    <p>Fast delivery across Peninsular and East Malaysia. We handle the logistics so you can focus on your business.</p>
                </div>
                <div class="benefit-card">
                    <h3>After-Sales Support</h3>
                    <p>Comprehensive warranty support and technical assistance. Our team troubleshoots and resolves issues quickly to minimize downtime.</p>
                </div>
            </div>
        </section>

        <section class="product-categories-detail">
            <h2>Complete Range of IT Products</h2>
            
            <h3>Computers & Laptops</h3>
            <p>Business desktops, high-performance workstations, and laptops from HP, Dell, Lenovo, Acer, and ASUS. Custom configurations available for enterprise deployments, including bulk orders with imaging and setup services.</p>
            
            <h3>Servers & Storage</h3>
            <p>Enterprise-grade servers (tower, rack, blade), NAS storage solutions, and data center hardware. We provide pre-configured servers ready for deployment with your preferred OS and software stack.</p>
            
            <h3>Networking Equipment</h3>
            <p>Routers, switches, access points, and firewalls from Cisco, MikroTik, Ubiquiti, TP-Link, and more. We design, supply, and configure your entire network infrastructure.</p>
            
            <h3>CCTV & Security Systems</h3>
            <p>IP cameras, NVR/DVR systems, access control, and alarm systems. Professional-grade surveillance solutions for offices, warehouses, retail, and industrial sites.</p>
            
            <h3>Printers & Peripherals</h3>
            <p>Multifunction printers, barcode scanners, label printers, monitors, keyboards, mice, UPS systems, and all IT accessories your business needs.</p>
            
            <h3>Software Licensing</h3>
            <p>Genuine Microsoft Windows, Office 365, antivirus, and business software licenses. Volume licensing available for enterprise and government clients.</p>
        </section>'''

CONTACT_EXTRA_CONTENT = '''
        <section class="why-contact">
            <h2>Why Work With Marz Technology?</h2>
            <div class="reasons-grid">
                <div class="reason-card">
                    <h3>20+ Years Experience</h3>
                    <p>Established since 2004, we have deep expertise across IT infrastructure, AI, cybersecurity, and digital transformation for Malaysian businesses.</p>
                </div>
                <div class="reason-card">
                    <h3>Free Consultation</h3>
                    <p>Get a no-obligation assessment of your IT needs. We will recommend the best solutions tailored to your budget and business goals.</p>
                </div>
                <div class="reason-card">
                    <h3>2000+ Happy Clients</h3>
                    <p>Trusted by over 2,000 businesses, government agencies, and enterprises across Malaysia. Check our testimonials and case studies.</p>
                </div>
                <div class="reason-card">
                    <h3>End-to-End Service</h3>
                    <p>From consultation and procurement to installation, training, and ongoing support — we handle everything so you don't have to juggle multiple vendors.</p>
                </div>
            </div>
        </section>

        <section class="faq-quick">
            <h2>Frequently Asked Questions</h2>
            
            <h3>How quickly can you respond to my inquiry?</h3>
            <p>We respond to all inquiries within 1 business day. For urgent matters, call us directly at +60-13-361-1046.</p>
            
            <h3>Do you provide on-site services?</h3>
            <p>Yes, we provide on-site IT support, installation, and consultancy services throughout Klang Valley and selected areas nationwide.</p>
            
            <h3>Can I get a customized quotation?</h3>
            <p>Absolutely. Tell us about your project, and we will prepare a detailed proposal with scope, timeline, and pricing tailored to your requirements.</p>
            
            <h3>What areas do you cover?</h3>
            <p>We serve clients across Malaysia including Kuala Lumpur, Selangor, Putrajaya, Johor, Penang, Melaka, and more. Remote support is available nationwide.</p>
        </section>'''

# ============================================================
# FILE UPDATES
# ============================================================

def patch_file(filepath, old, new):
    with open(filepath, 'r') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

def insert_after(filepath, marker, to_insert):
    """Insert text after the first occurrence of marker"""
    with open(filepath, 'r') as f:
        content = f.read()
    idx = content.find(marker) + len(marker)
    new_content = content[:idx] + to_insert + content[idx:]
    with open(filepath, 'w') as f:
        f.write(new_content)

# === HOMEPAGE (index.html) ===
print("=== Processing index.html ===")
# Add Organization + LocalBusiness + Breadcrumb after OG tags (before </head>)
insert_after("/tmp/marz-index.html", '    <meta property="og:image" content="https://marz.my/og-image.png">\n', 
    '\n' + ORGANIZATION_SCHEMA + '\n' + LOCALBUSINESS_SCHEMA + '\n' + 
    get_breadcrumb_schema([("Home", "https://marz.my/")]) + '\n')

print("index.html schemas added")

# === ABOUT ===
print("=== Processing about.html ===")
insert_after("/tmp/marz-about.html", '    <meta property="og:image" content="https://marz.my/og-image.png">\n',
    '\n' + get_breadcrumb_schema([
        ("Home", "https://marz.my/"),
        ("About", "https://marz.my/about.html")
    ]) + '\n')
print("about.html breadcrumb added")

# === SERVICES ===
print("=== Processing services.html ===")
insert_after("/tmp/marz-services.html", '    <meta property="og:image" content="https://marz.my/og-image.png">\n',
    '\n' + get_breadcrumb_schema([
        ("Home", "https://marz.my/"),
        ("Services", "https://marz.my/services.html")
    ]) + '\n' + FAQ_SERVICES_SCHEMA + '\n')
print("services.html breadcrumb + FAQ added")

# === AI SOLUTIONS ===
print("=== Processing ai-solutions.html ===")
insert_after("/tmp/marz-ai-solutions.html", '    <meta property="og:image" content="https://marz.my/og-image.png">\n',
    '\n' + get_breadcrumb_schema([
        ("Home", "https://marz.my/"),
        ("AI Solutions", "https://marz.my/ai-solutions.html")
    ]) + '\n' + FAQ_AI_SCHEMA + '\n')
print("ai-solutions.html breadcrumb + FAQ added")

# === PRODUCTS (expand + breadcrumb) ===
print("=== Processing products.html ===")
insert_after("/tmp/marz-products.html", '    <meta property="og:image" content="https://marz.my/og-image.png">\n',
    '\n' + get_breadcrumb_schema([
        ("Home", "https://marz.my/"),
        ("Products", "https://marz.my/products.html")
    ]) + '\n')
# Add extra content before </body>
insert_after("/tmp/marz-products.html", '    </body>', '\n' + PRODUCTS_EXTRA_CONTENT + '\n')
print("products.html breadcrumb + expanded content added")

# === CONTACT (expand + breadcrumb) ===
print("=== Processing contact.html ===")
insert_after("/tmp/marz-contact.html", '    <meta property="og:image" content="https://marz.my/og-image.png">\n',
    '\n' + get_breadcrumb_schema([
        ("Home", "https://marz.my/"),
        ("Contact", "https://marz.my/contact.html")
    ]) + '\n')
# Add extra content before </body>
insert_after("/tmp/marz-contact.html", '    </body>', '\n' + CONTACT_EXTRA_CONTENT + '\n')
print("contact.html breadcrumb + expanded content added")

print("\n=== ALL DONE ===")
for name in ["index", "about", "services", "ai-solutions", "products", "contact"]:
    wc = len(open(f"/tmp/marz-{name}.html").read())
    print(f"  /tmp/marz-{name}.html: {wc} chars")

PYEOF
