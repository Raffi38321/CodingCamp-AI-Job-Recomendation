import re
import io

import fitz  # PyMuPDF
import docx  # python-docx
import streamlit as st
import requests

skill_arr = ['SQL', 'Business Analysis', 'Relational Databases', 'System Analysis', 'Analytical Skills', 'SDLC', 'Requirements Analysis', 'Stakeholder Management', 'Cloud Platform System', 'Teamwork', 'Life Insurance', 'Business Process Improvement', 'Csm', 'Insurance', 'Group Asia', 'Life 400', 'Cbap', 'Tidak ada', 'Project Management', 'IT Management', 'MySQL', 'React.js', 'jQuery', 'HTML', 'Laravel', 'CLOUDFLARE', 'CDN', 'Jwt', 'PHP', 'JavaScript', 'Tailwind', 'GIT', 'Linux Server', 'Node.js', 'CSS', 'REST API', 'Go / Golang', 'Mobile App Development', 'Flutter', 'Next.Js', 'Restful API', 'C#', 'SAP', 'Oracle E-Business Suite (EBS)', 'Accounting', 'PHP Native', 'Backend Development', 'Oracle ERP', 'PostgreSQL', 'Java', 'MongoDB', 'Microsoft SQL Server', 'C++', 'Python', 'CI/CD', 'Jenkins', 'Amazon Web Services (AWS)', 'clean architecture', 'Micro Services', 'Rust', 'NoSQL', 'Google Cloud Platform', 'Bitbucket', 'Microservices Architecture', 'Core Java', 'VB.NET', '.NET', 'IT Infrastructure Management', 'ERP Software', 'Software Development', 'Software Engineering', 'Mobile Development', 'Mobile UI Design', 'Dart', 'TypeScript', 'Bootstrap', 'Docker', 'Android Development', 'Jrpc', 'Sass', 'github', 'LESS', 'TailwindCSS', 'Model-View-Controller (MVC)', 'Object-Oriented Programming (OOP)', 'Ajax', 'iOS Development', 'Swift Ui', 'Swift', 'Nginx', 'System Integration', 'Networking', 'Claude', 'Kubernetes', 'Firebase', 'Frontend Development', 'API Development', 'Leadership', 'Open Clow', 'Blackbox Ai', 'NestJS', 'gRPC', 'CSR', 'Ssr', 'Ionic Framework', 'Fullstack', 'GraphQL', 'Vue.js', 'WordPress Development', 'UIKit', 'Gin', 'Kotlin', 'UX Design', 'Code Review', 'Website Management', 'Web Development', 'Search Engine Optimization (SEO)', 'Web Analytics', 'Codeigniter', 'Spring Boot', 'Hardhat', 'Solidity', 'Foundry', 'Openzeppelin', 'Problem Solving', 'MariaDB', 'React Native', 'Agile Methodologies', 'SQLite', 'Scrum', 'Angular.js', 'Flask', 'Design Api', 'Odoo', 'ELK', 'Cyclic Redundancy Check (CRC)', 'Redux', 'Time Management', 'Technical Support', 'Troubleshooting', 'Help Desk', 'IT Support', 'Network Troubleshooting', 'Spring Framework', 'Github Version Control', 'Database Management', 'Postman Software', 'Backend Laravel', 'Express.Js', 'Advanced Programming Skills', 'Performance & Security Optimization', 'Messege Brokers', 'fullstack', 'Vite', 'UI Design', 'Back-End Web Development', 'AI Systems', 'Springboot', 'English Language', 'HTTPS', 'Ruby on Rails', 'IT Service Management', 'Web Design', 'WMS System', 'System Design', 'CodeIgniter', 'Websocket', 'Redis', 'ui/ux', 'Charting', 'Orderflow', 'Front-End Architecture', 'next js', 'Microsoft Azure', 'Interpersonal Skills', 'Computer Science', 'Attention to Detail', 'Communicative', 'ElysiaJs', 'MVVM', 'Native.js', 'JSON', 'Network Administration', 'Security System', 'Application Development', 'Figma', 'Authentication & Security (oauth2', 'Oidc', 'Jwt)', 'Build Tools (webpack Atau Vite)', 'State Management (zustand Atau Sejenisnya)', 'Api Integration (restful Api / Backend Services)', 'React.js / Next.js', 'Next.js', 'Communication Skills', 'Cloud Computing', 'Android Testing', 'Analisa Penagihan', 'penagihan', 'kolektor', 'Software Quality Assurance', 'Internet of Things (IoT)', 'Three.js', 'Microsoft Office', 'Mapping', 'Linux', 'PostGIS', '3D GIS', 'Gis Algorithms', 'Win32 Api', 'Winform', 'Objective-C', 'Cicd', 'Software Documentation', 'Pydantic', 'PHP Programming', 'fastAPI', 'Asynchronous Programming', 'Xcode', 'reactjs', 'Lavarel', 'Kafka', 'Nuxt.js', 'react js', 'vue js', '.NET CORE', 'RabbitMQ', 'Ai-assisted Development', 'Warehouse Management', 'Supply Chain Management', 'Retail Management', 'Celery', 'HTMX', 'HTTP', 'J2EE', 'Oracle Database', 'Jest', 'XML', 'Banking', 'Temenos24', 'DevOps', 'GCP', 'Socket.IO', 'ASP.NET', 'Collaboration', 'Nodejs', 'Ai Claude Code', 'Java Springboot', 'Software Architecture', 'Mentoring', 'Training', 'Agile Project Management', 'Microsoft Excel', 'IT Security', 'Echo', 'PrismaORM', 'gcp', 'SpringBoot', 'Intelij Idea', 'JUnit', 'Maven', 'Java springboot', 'RESTful API', 'RDBMS', 'Gorm', 'Prometheus', 'Grafana', 'Technical Leadership', 'Database Design', 'CentOS', 'Java SpringBoot', 'berpikir kritis', 'Kemampuan Menyesuaikan Diri', 'ECMAScript 6 (ES6)', 'Quarkus', 'AWS Lambda', 'Extract', 'Transform', 'Load (ETL)', 'Data Management', 'Automation Testing', 'Unit Testing', 'Eclipse', 'nodejs', 'ReactJS', 'ServiceNow', 'Project Implementation', 'ITSM', 'Strong Communication Skills', 'Testing Library', 'Claude Code', 'spring boot', 'SOAP', 'Apache', 'Microservis', 'Firebase Sdk', 'SwiftUI', 'Responsive Web Design', 'Communication', 'Vurjs', 'java spring boot', 'Hibernate', 'Azure', 'ROBOTIC PROCESS AUTOMATION', 'Microsoft Word', 'AI Tools', 'claude code', 'jest', 'Software Enggineering', 'Programmer', 'Full-stack', 'notepad', 'Tableau', 'Slik', 'Data Warehouse', 'Data Integration', 'Power BI', 'Data Visualization', 'ETL', 'SSIS', 'Data Modeling', 'Business Flow Understanding', 'Api & Integration', 'Odoo Technical Core', 'Database & Query', 'QA Automation', 'UiPath', 'Microsoft Power Platform', 'Robotic Process Automation (RPA)', 'Power Automate', 'Css / Javascript Animation (aos', 'Gsap', 'Atau Sejenisnya)', 'Html5', 'Css3', 'Javascript (es6+)', 'Responsive Web Design & Cross-browser Compatibility', 'Ui Slicing Dari Figma Ke Code', 'Odoo Website Module (v15/16/17)', 'outsystems', 'ISO 20022', 'Ui Framework', 'Unity3D', 'Augmented Reality', 'Middleware', 'Sequelize', 'SCSS', 'FLASK', 'django', 'Retrofit', 'MS SQL Server', 'Entity Framework (EF)', 'Web API', 'Konsep Object-oriented Programming (oop)', 'Codeigniter (ci)', 'RxJS', 'Api Integration', 'html5', 'Public Speaking', 'Presentation Skills', 'Visual Studio', 'CRM', 'Tokopedia Ads', 'Digital Marketing', 'Poster Design', 'Meta Ads', 'Scala', 'PL/SQL', 'LINQ', 'oracle apex', 'Google Sheets', 'Jira', 'Trello', 'Ruby', 'Caching', '.netcore', 'DevExpress', 'Orchestrator', 'Power Apps', 'Microsoft Power Automate', 'Robotics', 'Canva Design', 'CMS', 'Rpg As400', 'Salesforce', 'Information Technology', 'Administration', 'Office Administration', 'Data Analytics', 'Hard Worker', 'LLM', 'n8n', 'Graphic Design', 'Adobe Illustrator', 'Brand Design', 'Logo Design', 'Typography', 'Adobe Photoshop', 'Packaging Design', 'AutoCAD', '3D Modeling', 'Product Design', 'SketchUp', '3D Rendering', '3D Design', 'Enscape', 'Lumion', '3D Max', 'Blender', 'Vray', 'Creative Design', 'Design Thinking', 'Event Management', 'Corporate Communications', 'Offline Event Operation', 'Fashion Design', 'Pattern Making', 'Fashion Brand Sales', 'Color Theory', 'Book Layout', 'Editorial Layout', 'Team Management', 'Vector Illustration', 'CorelDRAW', 'Content Creation', 'Adobe Premiere Pro', 'Motion Graphics', 'Adobe After Effects', 'E-Commerce Photography', 'Photo Editing', 'Commercial Photography', 'Video Editing', 'Apparel Mass Production', 'Fashion Stylist', 'Graphic Illustrations', 'Adobe XD', 'Product Development', 'New Product Development', 'Customer Service', 'Production Management', 'Image Editing', 'Adobe Lightroom', 'Interaction Design', 'Desain Komunikasi', 'Photography', 'Rendering', 'Interior Design', 'Adobe InDesign', 'Motion Design', 'Social Media', 'Illustration', 'Videography', 'Capcut', 'Revit', 'Maya', 'SolidWorks', 'Textile Sampling', 'Sewing', 'Textile Design', 'Editor', 'Creative Writing', 'Dress Design', 'proactive', '3D Animation', '2D Animation', 'Autodesk Revit', 'Architectural Design', 'Fashion Editing', 'Artificial Intelligence', 'corel draw', 'Microsoft PowerPoint', 'Pattern Design', 'squarespace', 'Curriculum Development', 'Film & Video Production', 'H5P', 'Google Workspace', 'Multimedia Design', 'Lumi Education', 'Instructional Design', 'Articulate storyline', 'Page Layout', 'Social Media Content Design', 'Basic Motion Graphic (preferred)', 'Understanding Digital Marketing Visual Needs', 'Layout & Visual Composition', 'Ads Creative Design', 'Branding & Visual Identity Understanding', 'Content Editing', 'Team Leadership', 'Creative Strategy', 'Marketing Communications', 'Mechanical Design', 'Project Coordination', 'Visual Design', 'Audio Editing', 'Graphics And Text Layout', 'Creative Thinking', 'E-Commerce Graphic Designer', 'Ai Design Tools', 'key visual', 'Sketch', 'Positive Attitude', 'Content Strategy', 'Google Analytics', 'Google Ads', 'Graphic Designer', 'Interior and Exterior Design', 'E-commerce', 'Content Management', 'Target Oriented', 'TikTok', 'Initiative', '2d/3d', 'Photoshop', 'detail oriented', '3d Software', 'Visual Storytelling', 'Sales and Marketing', 'Electrical Design', 'Zuken E3', 'Elcad', 'E-base', 'Video Color Grading', 'Video Ad Creative', 'Creative Marketing', 'User Experience Design', 'Adobe Suite', 'Wireframing', 'Solid Wood Furniture', 'Content Writing', 'Client Services', 'Quality Control', 'Working under pressure', 'Brand Development', 'Corel draw', 'Design Promo', 'Product Packaging', 'adobe in design', 'Design Guideline', 'Design Campaign', 'UX Research', 'Discipline', 'Smart Lighting', 'Design Pencahayan', 'Electronic Components', 'Usability Testing', 'V-Ray', 'Design Grafis', 'Construction Site Management', 'Construction Management', 'Live Streaming', 'Live E-Commerce', 'Content Planning', 'Content Operations', 'Responsible', 'Computer Engineering', 'CAD', 'Mechanical Engineering', 'Data Entry', 'Content Marketing', 'Product Photography', 'Book Editing', 'News Editing', 'Copy Editing', 'Influencer Marketing', 'Customer Engagement', 'Video Recording', 'Video Content Operation', 'ZBrush', 'Unreal Engine', 'Digital Sculpting', 'News Writing', 'Copywriting', 'Editorial Illustrations', 'Short Video', 'Product Marketing', 'Concept Art', 'Content Products', 'Creative Planning', 'Short Video Production', 'Image Photo Retouching', 'Pengambilan foto', 'DaVinci Resolve', 'Music', 'Content Review', 'Social Media Analytics', 'Video Capture', 'initiative', 'Cinematography', 'Organizational Skills', 'Microsoft Outlook', 'Google Docs', 'Camera Operation', 'Lighting', 'Tiktok Affiliate', 'Portrait Photography', 'Animation', 'Script Writing', 'Visual Effects (VFX)', 'Fashion Videography', 'Fashion Photography', 'Capcut PRO', 'creative direction', 'dslr camera', 'content production', 'video editor', 'Direct Talent', 'AI Editor', 'Drone', 'Market Trends', 'Google Trends', 'Jenjang Karir', 'Dekat Transum', 'Bonus Kinerja', 'Media Planning', 'Instagram Marketing', 'Davinci Resolve', 'Affiliate Marketing', 'visual effects', 'camera', 'Riset Keyword', 'Localization', 'Chinese-English Translation', 'Chinese Language', 'English-Indonesian Translation', 'Data Analysis', 'Critical Thinking', 'Supermarket Cashier', 'Cashier', 'Credit Card Sales', 'Convenience Store Cashier', 'Storyboard', 'Host', 'Talk Show Host', 'E-Commerce Products', 'B2C Sales', 'Online Customer Service', 'B2B Sales', 'E-Commerce Customer Service', 'Computer Networking', 'Shopee Affiliate', 'Stock Opname', 'Order Management', 'Store Operation', 'Marketing Analytics', 'Customer Relations', 'Interpersonal Communication', 'Scheduling', 'Purchasing Negotiation', 'Industrial Purchasing', 'ESB', 'marketplace', 'Civil Engineering', 'Logistics Distribution', 'Logistics Management', 'Warehouse Operator', 'Administrative Logistics', 'Disiplin', 'Humble', 'Teliti', 'Mampur Berkomunikasi Dengan Customer', 'Telesales', 'accurate', 'Competitive Analysis', 'Shopee Ads', 'Filing Document', 'Detail Oriented', 'multitasking', 'Kepabeanan', 'Purchasing', 'Negotiation Skills', 'Procurement', 'Zoom', 'Google Drive', 'Market Research', 'Research Skills', 'Standard Mandarin', 'Halal Product Knowledge', 'Shopping Mall Cashier', 'Printing Operator', 'Keahlian Komunikasi.', 'Program Management', 'Report Writing', 'General Ledger Accounting', 'Invoice Processing', 'Budgeting', 'Financial Statements', 'Administrative Procurement', 'Tally', 'Accurate', 'Public Relations', 'Cross-functional Team Leadership', 'Computer Skills', 'Renovation Project Management', 'Operational Efficiency', 'Packing', 'B2C Marketing', 'Pre-Sale Bidding', 'Tender Preparation', 'Forecasting', 'Sales Operations', 'Jurnal Accounting System', 'Sales Analysis', 'Sales Management', 'Sales Strategy', 'Import Export', 'Customer Relationship Management', 'Management Reporting', 'Tech-savvy', 'teliti', 'Terbiasa dengan target', 'Marketing Strategy', 'Selling Skills', 'B2B Marketing', 'Marketplace', 'Ground Promotion', 'Channel Promotion', 'Kemampuan Penawaran', 'Warehouse Management System', 'Telecommunications', 'Cekatan dalam bekerja', 'Terbiasa Bekerja Dibawah Tekanan', 'Event Operations', 'Database Monitoring', 'Tax Reporting', 'Coretax', 'B2b Sales Support', 'spreadsheet', 'Pdf', 'Email Marketing', 'Contract Negotiation', 'Account Management', 'Data Monitoring', 'Customer Satisfaction', 'New Car Sales', 'Car Sales', 'canvassing', 'Live Streaming Sales', 'fast response', 'Data Reporting', 'Luwes', 'Store Display', 'Store Operations', 'Customer Support', 'Customer Acquisition', 'Pharmaceutical Sales', 'Healthcare Equipment Sales', 'Medical Devices', 'Healthcare Products Sales', 'Medical and Healthcare', 'Store Sales', 'Cold Calling', 'Sales Planning', 'Online Promotion', 'Business Negotiation', 'Gym Industry', 'Fitness', 'Business Development', 'Client Relations', 'Performance Management', 'Key Account Management', 'Multitasking', 'Taxation', 'Accounts Receivable', 'Online Sales', 'Jujur', 'Advertising Sales', 'Advertising Media', 'Electrical Engineering', 'Online Advertising', 'Facebook Ads', 'Canvassing', 'pemahaman produk', 'Administrasi Penjualan', 'Tax Accounting', 'Zahir Software', 'Corporate Tax', 'Tax Management', 'Income Tax', 'Financial Analysis', 'Bookkeeping', 'Corporate Finance', 'Accounts Receivable and Payable Accounting', 'Tax Planning', 'Internal Audit', 'Budget Management', 'Cost Control', 'Financial Management', 'MYOB', 'Accounts Payable', 'Xero', 'Financial Compliance', 'Tax Audit', 'admin finance', 'Lean Manufacturing', 'Cogs Or Cogm', 'Law', 'Finance Reporting', 'Accurate Online', 'Financial Report Audit', 'Adaptability', 'Cash Flow Management', 'Payroll Administration', 'Pelaporan Keuangan', 'COGS', 'Accurate Software', 'Human Resource Development (HRD)', 'Risk Management', 'HR Administration', 'Risk Analysis', 'Financial Planning', 'Risk Control', 'Human Resources Management', 'Legal Risk Control', 'Recruitment', 'Health Insurance', 'PPh 23', 'Bank Reconciliation', 'PPH 25', 'Rekonsiliasi Beban', 'Tax Compliance & Tax Advisory Skills', 'Communication & Professional Traits', 'Control', 'Governance & Risk Management', 'Leadership & Supervisory Skills', 'Business Partnering & Strategic Thinking', 'Financial & Accounting Expertise', 'Forecasting & Cashflow Control', 'System & Process Improvement', 'Account Payable', 'Managerial Finance', 'Education Administration', 'Cash Accounting', 'Logic Analyzer', 'Store Management', 'Property Management', 'Property Customer Service', 'Financial System Management', 'Financial Policy', 'Import and Export Logistics', 'Isak 35', 'System Operation And Maintenance', 'Fee Collection', 'Project Planning', 'Finane', 'Financial Advisory', 'Financial Consulting', 'Financing Management', 'Secretarial Skills', 'Valuation', 'Cost Management', 'Fraud Audit', 'Leadership Training', 'Business Strategy', 'Key Performance Indicators (KPI)', 'Performance Audit', 'PSAK', 'Strategic Thinking', 'financial planning and analysis', 'Strategic Planning', 'IFRS', 'Statistics', 'Database Systems', 'Data Engineering', 'Pyton/r', 'Logistics Settlement', 'Data analysis', 'Numerical Analysis', 'Google Data Studio', 'Phyton', 'Talend', 'Pentaho', 'Data Mart', 'Data Modelling', 'Looker Studio', 'Data Collection', 'Data Analyst', 'Sql Query', 'R Programming', 'KPI Reports', 'Data Quality', 'Microsoft Dynamics 365', 'Data Migration', 'Elasticsearch', 'Lucene', 'office 365', 'Pandas', 'Big Data Development', 'Cloudera', 'Strong Analytical & Problem-solving Skills', 'Data Analysis & Correlation', 'Sql & Python', 'Telecom Kpi Understanding', 'Dashboard & Visualization', 'Management Lead', 'Whatsapp Business API', 'Summarizing', 'tanggung jawab', 'Work Under Pressure', 'Operations Management', 'Google Spreadsheets', 'Python Numpy', 'PyTorch', 'Scikit-learn', 'Inventory Management', 'Business Process Optimization', 'Xlsx', 'CSV', 'Minitab', 'stata', 'IBM SPSS', 'Tunning  Process', 'Fixed Broadband Data', 'Exploratory Data Analysis', 'UML', 'Solution Architecture', 'Flowchart', 'Information Systems', 'System Architecture', 'OpenAI API', 'Data Cleaning', 'Business Process Mapping', 'Analytical Thinking', 'Data Structuring', 'Relational Database Management Systems', 'Basic SQL', 'Microsoft 365', 'Api First', 'Inter-service Communication', 'Cloud Integration', 'Data Flows', 'Business Process Modeling', 'IT Project Management', 'Dokumentasi Teknis', 'Komunikasi Lintas Divisi', 'Fast Respon', 'Spreedsheet', 'BRD', 'Accounting Knowledge', 'Fsd', 'Dokumen Prd. Fsd', 'Brd', 'Product Requirement Document (Prd)', 'Draw.io', 'Methodology: Waterfall And Agile Scrum', 'Business Requirement Document (Brd)', 'Tsd', 'Financial System Analyst', 'Google BigQuery', 'Process Improvement', 'Business Intelligence', 'Active Communication', 'Data Annotation', 'Data Linguist', 'Automation System', 'Data Processing & Data Handling', 'Programming Languages', 'Technical Writing', 'Brand Management', 'FGD', 'Quantitative Research', 'Qualitative Research', 'Notion', 'Kepemimpinan Tim Lintas Divisi', 'Interpersonal Skill', 'Analitik Data', 'Document Management', 'Writing Software Requirement Specification', 'IT Consulting', 'Query Sql Server', 'lark', 'Business Requirement Document', 'User Story', 'Memahami Sdlc Serta Metodologi Agile Dan Waterfall', 'Life Asia', 'AS 400', 'Database Development', 'Arsitektur System Payment', 'Lucidchart', 'Computer Hardware', 'Information Security', 'Network Security', 'Cybersecurity', 'Google Maps', 'Clm', 'core banking', 'Microsoft Teams', 'Confluence', 'Slack', 'Asana', 'Requirements Gathering', 'Architecture Design', 'Use Case', 'Natural Language Processing (NLP)', 'Machine Learning', 'Deep Learning', 'Legal Research', 'Legal Compliance', 'Corporate Law', 'English Label', 'Cambridge C1 Level', 'Cambridge B2', 'Business English', 'English Customer Service', 'Database & Sql', 'Script Automation', 'Basic Smartcard Knowledge', 'Programming Language (python / Java / C# / Js)', 'Automation Testing Tools', 'Debugging & Problem Solving', 'Computer Vision', 'Data Mining', 'Japanese Language', 'COBOL', 'Nextjs', 'Lean And Extreme Programming (xp)', 'code igniter', 'test case', 'QA Testing', 'Quality Assurance', 'Test Plan', 'Manual Testing', 'Katalon', 'Functional Testing', 'Bug Tracking', 'Regression Testing', 'API Testing', 'Tomcat', 'Kibana', 'Groovy', 'Software Installation', 'Clickhouse', 'Tauri', 'Integration Testing', 'Onnx', 'RedPanda', 'C', 'Hadoop', 'Data Processing', 'Apache Spark', 'airflow', 'Etl', 'AIRFLOW', 'Confluent', 'Docker & Container Lifecycle', 'Kubernetes (deployment', 'Scaling', 'Resource Tuning)', 'Monitoring & Logging Basic', 'Google Cloud Platform (compute', 'Network', 'Billing Awareness)', 'Ci/cd Pipeline (build → Deploy → Rollback)', 'Linux & Basic Networking', 'Data Orchestration', 'Etl/elt Pipeline', 'Olap Technology', 'Metabase', 'Big Data Architecture', 'Data Governance', 'Data Security', 'Aws S3', 'AWS GLue', 'Cassandra', 'Ms Power Automate', 'data streaming', 'SparkSQL', 'Star Schema Methodology', 'Cloud Data Services', 'Pyspark', 'phyton', 'Cloud Computing Architecture', 'Cloud Computing System Management', 'Data Pipeline', 'Software Testing', 'Performance Testing', 'Test Script', 'Regulation And Control Algorithm', 'Pemrograman', 'PLC Programming', 'HMI Programming', 'Industry Analysis', 'Industrial Engineering', 'Industrial Design', 'Industrial Automation', 'Looker', 'Remote Support', 'Ticketing System', 'Configuration Management', 'Change Management', 'Capacity Management', 'Hardware Maintenance', 'microsoft fabric', 'Memiliki Sertifikasi Jaringan Komputer Setara Internasional Ex: Ccna/ Mctna /setara Yang Masih Berlaku', 'Ansible', 'Bash', 'OpenStack', 'Hadoop Oozie', 'Oltp', 'Lakehouse', 'Ducklake', 'Airflow', 'HVAC', 'Security Audit', 'Penetration Testing', 'Gradle', 'CNC Operation', 'Llm Framework', 'Framework Backend Dan Frontend', 'Vector Database (chroma', 'Pgvector)', 'Snowflake', 'Superset', 'Open Metadata', 'NIFI', 'Neural Network', 'Openclaw', 'Claudecode', 'Pattern Recognition', 'Defect Management', 'Redshift', 'Prefect', 'dbt', 'K6', 'Api Performance Testing', 'Mechanical and Electrical BIM', 'kitchen equipment', 'Air Conditioning', 'Medallion Architecture', 'Delta Lake', 'Komponen Elektronik', 'MEP', 'Web Automation Testing', 'Load Testing', 'Model Context Protocol (mcp)', 'SAST/DAST', 'Certified Ethical Hacker (ceh)', 'Continuous Improvement', 'Engineering Consultant', 'Marketing Skills', 'Bahasa Mandarin', 'Research and Development (R&D)', 'Etl / Data Pipeline', 'Clickhouse Atau Hadoop', 'Indexing & Performance Tuning', 'Sql & Query Optimization', 'AI/ML', 'Zend Framework', 'Database Tuning', 'Sql Database', 'Api Design', 'Cisco', 'Firewall', 'Storage System', 'Storage Operation and Maintenance', 'LAN', 'Network Monitoring', 'Laboratory Skills', 'Chemical Analysis', 'Chemical Engineering', 'Chemical Testing', 'Operational Automation', 'Incident Management', 'Maplibre', 'Mapboxgl', 'Electricity', 'Maintenance Engineering', 'Prompt AI', 'terraform', 'Web Security', 'Woocommerce', 'Openshift', 'Google Kubernetes Engine', 'Cloud Run', 'Vertex Ai (gcp)', 'Engineering Practice', 'Ai Knowledge', 'Tech Stack', 'Fastapi', 'Technical Development', 'Mechanical Maintenance', 'Preventive Maintenance', 'Equipment Maintenance', 'Electrical Maintenance', 'Voip Knowledge', 'Server System Security', 'Event Modelling', 'Event Driven Architecture', 'Selenium WebDriver', 'Apache JMeter', 'Postman', 'Selenium', 'TOGAF', 'Implementation and Operation', 'Technology Consulting', 'Pre-Sales Technical Support', 'Active Directory', 'Office 365', 'ISO 22000', 'Chemical', 'Elektronika', 'IT Training', 'Kotlin Multiplatform', 'Electrical Installation', 'Electrical Wiring', 'Electrical Performance Test', 'Electrical Assembly', 'Power System', 'Software Ag', 'Webmethod', 'API Gateway', 'Business Management', 'Relationship Building', 'Business Planning', 'Construction Safety', 'Structural BIM', 'GD&T', 'Fusion 360', 'Driving', 'Kemampuan Analisa Market Dan Peluang', 'Kemampuan Teknis Engineering', 'Dapat Beradaptasi Dengan Mudah', 'Oil and Gas', 'Power Plane', 'Petroleum Engineering', 'Canvasing', 'Marine', 'Software Sales', 'Software Requirements Analysis', 'VMware', 'Veaam', 'presales', 'Engineer', 'ETABS', 'ISO 9001 2015', 'ISO 45001', 'ISO 14001 2015', 'Pemasaran B2g', 'TensorFlow', 'Terraform', 'Encryption', 'Postal Application (Point of Sales)', 'Algorithms', 'Payment Product Operation', 'Payment Security Standards', 'Certificate Management', 'Financial Security', 'Decryption', 'Playwright', 'Community Engagement', 'Good Documentation Skill', 'Campaign Management', 'Paid Advertising', 'Advertising Creativity', 'Maintanance Situs Web', 'TikTok Ads', 'Landing Page', 'cpas', 'Advertising Planning', 'A/B Testing', 'E-Commerce Operations', 'Instagram Ads', 'Marketing Management', 'Online Marketing', 'Performance Ads', 'Marketplace Management', 'Pay Per Click (PPC)', 'shopee ads', 'Graphic Design & Visual Content', 'Seo & Web Maintenance', 'YouTube Marketing & Management', 'International Business', 'New Business Development', 'SEMrush', 'Media Relations', 'Media Buying', 'Event Planning', 'KOL Operation', 'Manage Kol', 'membuat konten', 'edit video', 'KOL Management', 'Ads Budget', 'Content Creator', 'Telemarketing', 'Searh Engine Marketing', 'Experience Handling Ota', 'Selling', 'live chat', 'Call Center', 'Outbound Call', 'Memiliki Handphone Dan Laptop Pribadi', 'PPIC - Production Planning', 'Upselling', 'Customer Experience', 'Travel Sales', 'Travel Management', 'Travel Itinerary Planning', 'Printing Management', '3D Printing', 'Psychological Assessment', 'Ecommerce', 'Virtual Chat', 'Diligent', 'Inbound call', 'Mengetik Cepat', 'Internal Communications', 'Technology', 'Knowledge Management', 'Mathematics', 'Active Learning', 'Active Listening', 'Healthcare', 'Online Travel Agent', 'Hospitality Management']
kategori_arr =  ['System Analyst', 'Business Analyst', 'Tidak ada', 'Full Stack Developer', 'Mobile Developer', 'Software Architect', 'Backend Developer', 'Flutter Developer', 'iOS Developer', 'Frontend Developer', 'Technical Partner', 'Android Developer', 'Posisi Backend Lainnya', 'Database Administrator', 'Desainer Grafis & Brand', 'Desainer 3D', 'Fashion Designer', 'Visual Designer', 'UI/UX Designer', 'Packaging Designer', 'Desainer Interior', 'Desainer Tekstil', 'Arsitek', 'Web Designer', 'Posisi Pelatihan Khusus Lainnya', 'Desain Kurikulum', 'Lighting Designer', 'Staff Multimedia', 'Content Creator', 'Electrical & Mechanical Engineer', 'Editor Video & Film', '3D Modeler', 'Supervisor Konstruksi', 'Livestreamer', 'Desainer CAD', 'Film & Video Editor', 'Digital Marketing Specialist', 'Editor', '3D Artist', 'Videographer', 'Photo Editor', 'Independent Distributor', 'Graphic & Brand Designer', 'Administrative Staff', 'Multimedia Designer', 'Photographer', 'Product Marketing', 'Copywriter & Copyeditor', 'Other Media Positions', 'Data Entry Clerk', 'E-Commerce Operations', 'Accounting Admin', 'Sales Representative', 'Marketing Professionals', 'Sales Promoter', 'Sales Operations', 'Sales Marketing', 'Sales Counter', 'Sales Consultant', 'Other Sales Positions', 'Media Sales', 'Sales FMCG', 'Direct Sales', 'Sales Executive', 'Health Consultant', 'Telemarketer', 'Sales Manager', 'Business Development Executive', 'Tax Accountant', 'Finance Manager', 'Accountant', 'Finance Staff', 'Other Banking Positions', 'Finance Admin', 'Other Accounting Positions', 'Insurance Agent', 'Property Administrator', 'Secretary', 'Data Analyst', 'Other Backend Positions', 'Marketing Analyst', 'Data Engineer', 'Business Operations', 'Cybersecurity', 'IT Support', 'Data Scientist', 'Legal Specialist', 'QA Engineer', 'Devops Engineer', 'AI Engineer', 'Technical Manager', 'Technical Support Engineer', 'Industrial Engineer', 'Automation Engineer', 'HVAC Engineer', 'Mechanical Design Engineer', 'System Security', 'Civil Engineer', 'Mechanical Engineer', 'Network Engineer', 'Chemical Engineer', 'Field Application Engineer (FAE)', 'Other Artificial Intelligence Positions', 'Maintenance Engineer', 'Project Manager', 'Implementation Consultant', 'Product Manager', 'Electrical Engineer', 'Solar Engineer', 'Construction Worker', 'Growth Marketing', 'CAD Designer', 'Civil Engineering Manager', 'Technology Consultant', 'Site Reliability Engineer', 'Marketing Manager', 'Customer Service Representative', 'Call Center Agent', 'Travel Agent', 'Printing & Typesetting', 'Health Administrator']
industri_arr = ['Information Technology and Services', 'Tidak ada', 'Pharmaceuticals', 'Retail', 'Marketing and Advertising', 'Insurance', 'Printing', 'Automotive', 'Architecture & Planning', 'Education Management', 'Real Estate', 'Construction', 'Management Consulting', 'Leisure, Travel & Tourism', 'Internet', 'Public Relations and Communications', 'Computer Software', 'Sports', 'Events Services', 'Staffing and Recruiting', 'Packaging and Containers', 'Manufacturing', 'Investment Management', 'Media Production', 'Human Resources', 'Biotechnology', 'Logistics and Supply Chain', 'Professional Training & Coaching', 'Computer & Network Security', 'Primary/Secondary Education', 'Financial Services', 'Telecommunications', 'Health, Wellness and Fitness', 'Building Materials', 'Banking', 'Mechanical or Industrial Engineering', 'Market Research', 'Consumer Electronics', 'Business Supplies and Equipment', 'Legal Services', 'Hospital & Health Care', 'Outsourcing/Offshoring', 'Graphic Design', 'Import and Export', 'Oil & Energy', 'Design', 'Publishing', 'Broadcast Media', 'Distributor', 'Apparel & Fashion', 'Medical Practice', 'Computer Games', 'Hospitality', 'Facilities Services', 'Food & Beverages', 'Consumer Goods', 'Furniture', 'Sporting Goods', 'Online Media', 'Consumer Services', 'Textiles', 'Glass, Ceramics & Concrete', 'Animation', 'Package/Freight Delivery', 'Electrical/Electronic Manufacturing', 'Arts and Crafts', 'Higher Education', 'Entertainment', 'Public Safety', 'Capital Markets', 'Restaurants', 'Renewables & Environment', 'Food Production', 'Cosmetics', 'Fast-Moving Consumer Goods (FMCG)', 'Luxury Goods & Jewelry', 'Information Services', 'Wholesale', 'Music', 'Photography', 'E-Learning', 'Motion Pictures and Film', 'Accounting', 'International Trade and Development', 'Plastics', 'Translation and Localization', 'Computer Hardware', 'Local Trading', 'Chemicals', 'Commercial Real Estate', 'Warehousing', 'Machinery', 'Environmental Services', 'Farming', 'Mental Health Care', 'Law Enforcement', 'Individual & Family Services', 'Fund-Raising', 'Supermarkets', 'Paper & Forest Products', 'Mining & Metals', 'Medical Devices', 'Transportation/Trucking/Railroad', 'Aviation & Aerospace', 'Maritime', 'Program Development', 'Military', 'Alternative Medicine', 'Shipbuilding', 'Non-Profit Organization Management', 'Civic & Social Organization', 'Venture Capital', 'Tobacco', 'Industrial Automation', 'Research', 'Civil Engineering', 'Nanotechnology', 'Computer Networking', 'Government Relations', 'Performing Arts', 'Law Practice', 'Security and Investigations', 'Railroad Manufacture', 'Airlines/Aviation', 'Executive Office']
judul_arr = ['IT Business Analyst', 'IT System Analyst', 'IT Business Analyst - Insurance exp', 'IT Business Analyst (for Insurance industry)', 'Tidak ada', 'IT Business Analyst - ASAP (WFO Jakarta Area)', 'Software Developer', 'IT Software Developer Supervisor', 'Programmer for Software Developer', 'Junior Software Developer - Salesforce', 'Software Developer - Banking Industry', 'Software Developer (UiPath RPA)', 'Software Developer Engineer C and C++', 'Flutter Developer', 'Full Stack Developer', 'Web Developer', 'Fullstack Developer', 'iOS Developer', 'Fullstack Web Developer', 'Web Developer Laravel (Outsourcing)', 'C++ Software Engineer', 'Junior Software Engineer', 'Software Engineer (Fullstack)', 'Mobile Developer', 'Senior Software Engineer', 'Fullstack Developer (Middle)', 'Intern Fullstack Developer', 'IOS Developer', 'IT (Full Stack Developer)', 'Full Stack Developer (Jakarta & Bali)', 'Internship Fullstack Developer (PAID)', 'Full Stack Developer Intern', 'Software Engineer', 'Web Developer Intern', 'Full-Stack Developer (Web & Mobile)', 'Pengembang Web Developer (Laravel & Wordpress)', 'Full Stack Developer Intern (Unpaid)', 'Software Engineer (Bootcamp)', 'Staff Full Stack Developer jogja', 'Software Engineer II', 'Full Stack Developer (React & ExpressJs)', 'Senior Web Developer', 'Senior Fullstack Developer (Golang & React)', 'Fullstack Web & Mobile Developer', 'Fullstack Developer (Spring & Angular or React)', 'Fullstack Developer (NodeJS & Express.Js) - English Speaker', 'Full Stack Developer (workflow & Automation)', 'Full Stack Developer (Go, Kotlin, NextJs) - WFH', 'Dev Ops', 'software Engineer', 'Senior Full Stack Developer (On-Site Required)', 'Fullstack Developer (.NET Angular Selenium)', 'FullStack Developer (Angular, Java Springboot )', 'Full Stack Developer - Mid to Senior Level (3+ Years Experience)', 'Fullstack Developer (Ruby on Rails)', 'Junior Full Stack Web Developer', 'Fullstack Developer (New System Development – Migration Project)', 'Mobile Developer (Flutter)', 'Web Developer (React - Onsite)', 'Web Developer Internship (Unpaid)', 'INTERNSHIP (Junior Full Stack Developer)', 'FrontEnd Developer', 'Frontend Web Developer', 'Frontend Developer (React JS)', 'Frontend Developer (Reactjs, Nuxtjs)', 'Frontend Developer - Internship', 'Frontend Engineer', 'FrontEnd Engineer', 'Frontend Developer (Insurance Company Financial Services)', 'Senior Frontend Engineer', 'Front-end Developer', 'Front End Developer', 'Frontend Vue.JS', 'Frontend Engineer (Yogyakarta)', 'Front-end Developer(Flutter)', 'Front-end Developer (Internship)', 'Front-end Engineer', 'Software Engineer - Frontend', 'Internship Front End Developer (Vue js Ver 3)', 'Senior Fullstack Web Application Developer', 'Frontend (React Native & Android) - Banking Syariah', 'Front End Programmer', 'Frontend (React Native & Android) - Loc: Jakarta Utara', 'Odoo Developer', 'RECOVERY FRONT END ASSET', 'Internship Front End Programmer', 'React Js developer', 'IT Developer (Project Based)', '[IOT] Fullstack Developer - Middle Level', 'IT Fullstack Java Developer', 'Senior Fullstack Developer', 'Magang Fullstack Developer', 'Remote Senior Developer', 'Senior iOS Developer', 'IT DEVELOPER (Intern)', 'FULL STACK DEVELOPER', 'Fullstack Developer (Intern)', 'IT System Developer', 'Backend Developer', 'Senior Backend Developer', 'Backend Golang Developer', 'Golang Backend Developer (Hybrid)', 'Backend Developer Senior', 'Backend Developer (Golang)', 'Backend Java Developer', 'backend developer', 'Phyton Backend Developer', 'Backend Developer - Golang', 'Backend Developer (Next.js)', 'Backend Developer (.NET)', 'Backend Developer (Middle)', 'Backend Developer Intern', 'Backend Developer (ASAP)', 'Freelance Backend Developer', 'Backend (NodeJs) Developer', '[INTERN] Backend Developer', 'Backend Developer (Nodejs Expressjs)', 'Backend Developer - .NET Core', 'Backend Developer (Java Springboot)', 'Backend Developer (Java, Rust, Golang)', 'Backend Developer - Malaysia Relocation', 'Back-end Developer', 'Backend Developer (Java Spring Boot)', 'Backend Developer (Golang) - for Banking Industry', 'Backend Developer - Banking Client (Springboot)', 'Backend .Net Developer', 'Backend Engineer', 'BACKEND DEVELOPER MAINTENANCE', 'Back End Developer', 'Golang Developer', 'BackEnd Engineer', 'Senior Backend Engineer', 'Backend Developer (Golang) - Prefer ASAP (WFO Sudirman)', 'Internship Back End Developer (Golang)', 'Backend Engineer (Java Springboot)', 'Software Developer (Golang Developer)', 'Backend Dev (Java Springboot)', 'Senior Back-end Engineer', 'Java Developer', 'Backend PHP', 'Backend DevOps', 'Backend Springboot', 'Golang Developer - Banking', 'Backend Developer (Node.js) - Prefer ASAP, WFO Jakarta area', 'Backend Engineer (Yogyakarta)', 'Backend Python', 'golang developer', 'Junior Programmer Backend (Laravel)', 'Frontend Developer (Mobile Developer)', 'Senior Backend API Engineer', 'NodeJS Developer', 'Java Developer - Springboot', 'Back-end Developer - Super Apps', 'Java developer', 'Golang Developer - Banking Syariah', 'PHP Developer', 'Angular Developer', 'Senior Backend Engineer (Java, Lambda)', 'Back End Developer (Java Springboot) - Insurance Industry', 'Back-end Engineer', 'Back-end Developer (Node.js + Express.js)', 'Senior Frontend Developer', 'Back-end Developer (Insurance Company Financial Services)', 'Java Developer - Insurance', 'Back End Developer (Java Springboot) - Loc: Jakarta Utara', 'Senior .Net Developer', 'Fullstack Golang Developer  (React + Golang)', 'ServiceNow Developer', 'Junior Developer', 'Frontend Developer Senior', 'Junior Golang Developer - ASAP for Banking', 'Java Developer (Project Based)', 'Java Developer (Quarkus)', 'IT Java Developer', 'Java Developer (Life Insurance)', 'Frontend Developer', 'Back-end (Golang) Intern', 'Technical Lead Java Developer', 'Developer', 'iDempiere Developer', 'Developer Officer', 'PHP Laravel Developer - ASAP (WFO South Jakarta)', 'Technical Consultant (Developer)', '.Net Developer', 'Developer Manager', 'SQL Developer', 'Software Engineer Java Developer', 'ETL Developer', 'Odoo developer', 'RPA Developer', 'odoo developer', 'OutSystems Developer', 'Senior Fullstack Developer Associate', 'Back end Intern (Golang)', '.NET Developer (Bekasi Area)', 'Augmented Reality Developer', 'React Native Developer', '.NET Developer', 'Junior .NET Developer', 'Middleware Developer', 'Power BI Developer', 'Fullstack Developer (Laravel-Vue-MSSQL)', 'Front End Developer (Medior)', 'Java Springboot Developer', 'Junior Software Developer', 'Fullstack Developer (Mobile First)', 'Backend Software Engineer (Growth Path to Ruby on Rails)', 'Android Developer (automotive industry)', 'Android Java Developer', 'SENIOR DEVELOPER', 'NET Developer', 'FullStack Developer', 'Fullstack Developer (Internship)', 'Frontend Developer - Angular', 'Senior .NET Developer', 'Lead Developer', 'Full Stack Developer Internship', 'Full-stack Developer (.Net)', 'Python Developer (Project Based)', 'IT Bootcamp Software Developer Jakarta', 'Full Stack Developer & SEO', 'Backend Engineer (Onsite in Medan)', 'Oracle APEX Developer', 'IT Developer (Fullstack)', 'Mobile Developer (React Native)', 'IT Full Stack Developer', 'Application Developer (.NET)', 'Frontend Developer - Banking', 'RPA Developer - Telecommunication Industry', 'Senior VB.NET Developer (Outsource)', 'Ruby on Rails Developer', 'ReactJS Developer', 'WEB DEVELOPER', 'Junior developer', 'RPG AS400 Developer', 'Junior Salesforce Developer', 'IT Developer', 'Database Developer', 'remote sofware developer', 'Senior Front End Developer', 'Fullstack Developer (financial company)', 'Senior Full Stack Developer', 'Senior VB.NET Developer', 'JUNIOR FULLSTACK', 'Web Developer (Java, Golang + Rust) - Banking Industry', 'Grapic Designer', '3D Designer', 'Frontend Designer', '3D DESIGNER', '3d designer', 'Designer fashion', 'Graphic Designer', 'fashion designer', 'Fashion Designer', 'Footwear Designer', 'Creative Designer', 'Packaging Designer', 'Desainer Grafis', 'INTERIOR DESIGNER', 'GRAPHIC DESIGNER', '3D Product Designer', 'Interior 3D Designer', 'Graphic Designer Intern', 'Multimedia Designer', 'Visual Designer', 'APPAREL GRAPHIC DESIGNER', 'Product Designer - Packaging', '3D Designer (Exhibition)', 'Textile Designer', 'pattern designer', 'Senior Motion Designer', '[Intern] Graphic Designer', 'Architectural Designer & Interior Designer', 'Designer', '2D Designer', 'Fashion Designer (Junior)', 'Visual Graphic Designer', 'DESIGNER', 'Experienced Fashion Designer', 'Internship Graphic Designer', 'graphic designer junior', 'Web Designer', 'Curriculum Designer', '3D Event Designer', 'DESIGNER FASHION', 'Instructional Designer', 'Architectural Designer', 'Graphic Designer 3D', 'Senior Graphic Designer', 'Lighting Designer', 'Photobooth Designer', 'Graphics Designer', 'Graphic Designer 2D & 3D', 'FASHION DESIGNER INTERN', 'Graphic Designer Offline Activation', 'Graphic Designer Intern (Hybrid)', 'Interior Designer', 'Content Designer', 'Graphic Designer Internship', 'Intern Graphic Designer', 'Graphic Designer - Event Planner', 'Marketing Interior Designer', 'Graphic Designer Supervisor', 'Architectute Designer', 'Senior Electrical Designer', 'Creative Intern (Video Designer)', 'Freelance Graphic Designer', 'DESAINER GRAFIS', '3D & Motion Designer', '3D Booth Designer', 'Product Designer Internship', 'graphic art designer', 'Senior Interior Designer', 'Staff Graphic Designer', 'Graphic Designer Staff', 'Spatial & Product Designer', 'Social Media & Graphic Designer - Properland', 'Creative Marketing Designer', 'Desainer Grafis Sublim printing', 'UIUX Designer', 'Lighting Systems Designer', 'Designer 3 Dimensi', 'Junior Graphic Designer', 'Designer Interior', 'Intern Designer', 'Product Designer', 'Multimedia Designer Intern', 'Project Designer', 'Creative Designer (Design & Photography)', 'Event Spatial Designer', 'Designer (Internship)', 'content designer', 'Intern-Visual Designer', 'CAD Designer', 'Admin & Designer', 'Graphic Designer & Video Editor (Content Creator)', 'Editor Video', 'Editor', 'Content Creator & Editor', 'EDITOR', 'editor', 'Editor & Content Creator', 'Video Editor', 'video editor', 'VIDEO EDITOR', 'Videografer & Editor', 'EDITOR VIDEO', 'Editor entertainment', 'Videographer + Editor', 'Content Editor', 'Fotografer & Editor', 'Content & Editor', 'Video editor', 'content editor', 'Editor capcut', 'Videographer & Editor', 'Editor & Videographer', 'Content Creator dan Editor', 'Content Editor (Video & Visual)', 'Photographer and Video Editor', 'Content Creator & Video Editor', 'Graphic Design & Video Editor', 'Editor Video Konten', 'Editor Konten Video & Admin', 'Editor & Talent', 'Editor Buku', 'Freelance Video Editor', 'Kameramen & Editor', 'Multimedia & Video Editor', 'VIDEOGRAPHER & EDITOR', 'Video Editor Intern', 'eCommerce Video Editor', 'Videographer and Editor', 'Photografer & Editor Professional', 'Editor Foto', 'Graphic Design & Video Editor internship', 'Desain Grafis & Editor', 'Photographer Videographer & Editor', 'Editor Video & Design', 'Videographer & Video Editor', 'Photo & Videographer Editor', 'Editor Video Capcut', 'Video Editor & Videographer', 'Editor Video dan conten creator', 'Desain Grafis & Video Editor', 'Creative Copywriter & Video Editor', 'Video Editor (Ads + Creatives)', 'Staff Photo,Video & Editor', 'VIDEO EDITOR & CONTENT CREATOR', 'Content creator & editor magang', 'Videographer & Editor Content Creator', 'Video Editor Part-time', 'Videographer dan Video Editor', 'Video Editor Internship', 'Video & Photo Editor (Internship)', 'Photo and Video Editor', 'Videographer & Editor Internship', 'Photo Editor - Night Shift', 'Photo Editor - Day Shift', 'Editor and Graphic Designer', 'Editor sosial media', 'YouTube Video Editor', 'editor foto video', 'Video Editor (Hybrid)', 'Video Editor-Intern', 'SEO Content Editor Internship', 'Videographer & Video Editor Internship', 'Video Editor Content Creator', 'Video editor & Graphic Design', 'Desain grafis & Video Editor', 'Video Editor (CapCut)', 'Video grafer & editor', 'Video Editor [Paid Intern]', 'Video Production & Editor', 'Short Video Editor', 'Editor Video Intership', 'Videographer & Editor Intern', 'Videografer dan video editor', 'Content Creator + Editor', 'Editor Creative Intern', 'Graphic & Video Editor', 'Video Creative Editor', 'Videographer & AI Editor', 'CONTENT CREATOR (FOTO & VIDEO EDITOR)', 'photographer videographer editor', 'VIDEOGRAPHER & EDITOR INTERNSHIP', 'Editor Konten', 'Design Grafis dan Video Editor', 'Editor dan Videographer', 'Content editor', 'Digital Marketing', 'Kreatif Videografi Editor', 'VFX Editor', 'Videographer & Editor.', 'Editor Artikel', 'editor video', 'Content Creator, Editor, dan Video Editor Staff', 'editor and videographer', 'Editor & Admin Social Media', 'Script Editor (Storyline & Film)', 'Content Creator & Editor Product', 'Video Editor (Adobe Suite)', 'Dubbing Script Editor', 'Asisten Video Editor', 'Freelance Videographer & Editor', 'Magang Editor Jurnal', 'Social Media Strategist & Brand', 'VIDEOGRAFER & EDITOR', 'VIDEO EDITOR - ASISTEN KONTEN KREATOR', 'Photo Editor  - Yogyakarta', 'Staff Admin E - Commerce', 'Admin E-commerce', 'Admin E-Commerce', 'Admin e-commerce', 'admin e commerce', 'ADMIN E-COMMERCE', 'Admin E-commerce Marketplace', 'Admin E-Commerce Marketplace', 'Admin Data', 'admin proyek', 'Admin logistik', 'Admin Logistik', 'Admin Support', 'Admin Tiktok', 'Admin Kantor', 'ADMIN E-commerce', 'Admin kantor', 'Admin Purchasing', 'Admin Toko', 'Staf Admin Purchasing', 'Admin Proyek', 'Admin E-Commerce, Social Media & Sales', 'Staff Admin', 'Admin Data Entry', 'ADMIN PROYEK', 'Admin Penjualan', 'Admin Sosial Media', 'Admin E-Commerce Olshop Promosi & Design Produk', 'Staff admin', 'STAFF ADMIN', 'Admin penjualan', 'Staf admin', 'Admin Penjualan - Restoran', 'Admin Purchasing Produksi', 'Admin toko', 'ADMIN PURCHASING (Harian)', 'admin olshop', 'Admin Sosial Modia', 'Admin', 'ADMIN OLSHOP & LIVE', 'ADMIN SOSIAL MEDIA', 'Staf Admin', 'Marketplace Operator & Admin Kantor', 'Staff Admin Produksi', 'Admin Staff', 'Dicari Staff Admin Purchasing', 'Admin Logistik Cost', 'Admin purchasing', 'admin', 'Staff Admin Operasional', 'Admin Data & GA', 'STAF ADMIN', 'Admin Shopee dan Tiktok', 'Admin Kantor Pengacara', 'Staf Admin Purchasing Support.', 'Admin sosial media', 'Admin Support (Internship)', 'Staff Admin Penjualan', 'Admin staff', 'ADMIN PENJUALAN', 'Admin CCTV', 'EVENT ADMIN OFFICER', 'Admin Counter', 'Admin Marketplace', 'ADMIN STAFF', 'ADMIN MARKETING', 'ADMIN ACCURATE', 'Admin Purchasing Intern', 'General Admin', 'Admin Teknisi', 'Freelance Admin Purchasing', 'admin sosial media', 'admin penjualan', 'Head Admin', 'ADMIN PROJECT', 'Admin Project', 'Admin CRM', 'Operational Admin', 'Admin Gudang', 'Admin Analyst', 'Admin Online', 'Project Admin', 'Admin marketplace', 'Admin Proyek Kontraktor', 'Admin Magang', 'Admin Data Analist', 'Admin dengan kemampuan 3 bahasa: Jerman, Inggris, dan Indonesia', 'Admin Operasional', 'Admin Purchasing & AP', 'Admin Platform', 'Admin Stock', 'ADMIN', 'Staf Administrasi', 'Admin Lelang', 'ADMIN SUPPORT', 'STAFF ADMIN (PEREMPUAN)', 'ADMIN TOKO', 'Presales Admin', 'Admin Warehouse', 'Sales Administrator', 'Admin Sales Online', 'Sales Counter', 'Sales Representative', 'Export Sales Administrator', 'Admin Sales (Sales Support)', 'Sales Administrator (Business to University)', 'SALES COUNTER & ADMINISTRASI', 'Sales Executive', 'Admin sales online', 'Sales Administration', 'Admin - Sales', 'Sales Admin', 'Admin Sales', 'ADMIN SALES', 'Administrasi Sales', 'admin sales', 'Sales & Marketing Admin (Paid Internship)', 'Sales Marketing', 'SALES ADMIN', 'Sales Administrator di Jakarta Selatan - E-RAP', 'Admin Sales & Marketing', 'Admin Sales Support', 'Product Sales Executive', 'Admin Sales Processing', 'ADMIN SALES (BANDUNG)', 'Sales Support Admin', 'Admin Sales Officer', 'Magang Admin Sales', 'Admin Sales (Medical)', 'Sales Promotor Kredivo - YOGYAKARTA', 'Sales Promotor', 'Admin sales', 'Admin Sales (Leasing Cashier)', 'Sales Taking Order', 'Administration Sales', 'SALES TAKING ORDER', 'Admin Sales - Batch 2', 'Admin Sales & Marketing Communication', 'sales admin', 'Admin E-Commerce (Sales Online)', 'Admin Affiliate & Sales Support', 'ADMIN ONLINE SALES (FURNITURE)', 'SALES ADMINISTRATOR', 'Sales admin', 'Marketing and Sales Admin Intern', 'Marketing Sales', 'Sales Admin Intern', 'Sales Canvassing', 'Sales Admin Officer', 'Admin Sales Internasional', 'Sales Admin Marketplace', 'Sales Admin & Support', 'SALES GENERALIS PENEMPATAN CIREBON', 'Administrasi Support Penjualan', 'sales canvassing', 'Admin Sales & Packing', 'Sales Consultant', 'IT Sales Admin', 'Sales Admin Internship', 'Sales Merchandiser', 'Admin Sales Surabaya', 'Admin Sales Project', 'Retail sales and admin area (all Indonesia)', 'Sales & Business Development Admin', 'sales taking order', 'Admin Sales Online & Offline', 'Sales Mobil', 'Administrasi Sales Jakarta Barat', 'Sales Outboard Motor', 'Admin Sales Online Shop', 'Admin Executive (Sales)', 'SALES TO', 'Admin Sales Surakarta', 'admin sales pengelola ecommerce', 'Sales Taking Order (TO)', 'Admin Sales Accurate', 'Sales TO', 'Sales promotor', 'Sales Retail', 'Admin Sales for Marine', 'Admin Sales (Reseller & Marketplace)', 'sales retail', 'sales promotor', 'Admin Sales Percetakan', 'Fitness Consultant (Sales)', 'SALES GENERALIS BANK MANDIRI PENEMPATAN KARAWANG', 'SALES GENERALIS BANK MANDIRI PENEMPATAN BANDUNG', 'SALES GENERALIS BANK MANDIRI PENEMPATAN SUKABUMI', 'Admin Sales (Cilacap)', 'Sales Consultant Jannah Travel', 'Sales Online', 'Sales Associate', 'Sales Alat Selam (Diving)', 'Sales Promotor Kredivo JABODETABEK (Sales Retail Fashion)', 'Sales Taking Order General Trade', 'Area Sales Manager', 'Sales Mikro Bank DKI (Jabodetabek)', 'Staff sales & marketing', 'Sales Horeca', 'Sales Engineer', 'sales staff', 'Administrasi sales', 'Area Sales Supervisor', 'SALES CANVASSING', 'SALES GENERALIS (PENEMPATAN TASIKMALAYA, CIAMIS, DAN GARUT)', 'SALES GENERALIS (PEMATANGSIANTAR, RANTAU PRAPAT DAN SIBOLGA)', 'Admin sales online & customer service', 'Staff Sales Marketing', 'Sales Taking Order Produk Cat', 'Finance Accounting Tax', 'Manager Finance, Accounting & Tax', 'FINANCE, ACCOUNTING, TAX', 'Finance Accounting & Tax', 'Manager Finance Accounting & Tax', 'Finance, Accounting, Tax', 'Manager Finance Accounting Tax', 'Finance Accounting Tax Manager', 'Finance Accounting tax', 'Staff Finance Accounting Tax', 'Asisstant Manager Finance Accounting & Tax', 'Admin Finance', 'Finance Officer', 'Finance, Accounting & TAX', 'Finance, Accounting & Tax Manager', 'finance admin', 'Finance,Accounting & Tax', 'Finance Accounting & Tax Manager', 'Finance, Accounting & Tax (Mandarin)', 'Finance Accounting Tax Staff', 'Staff Finance, Accounting, & Tax', 'SPV Finance Accounting Tax', 'Finance, Accounting & Tax', 'Finance Operation', 'Finance Accounting Tax Officer', 'Administrasi & Finance', 'Admin (Finance & Sales)', 'Finance, Accounting, Tax, Supervisor', 'Finance Admin', 'FAT Manager (Finance, Accounting & Tax)', 'Finance Administrator', 'Finance Accounting & Tax (FAT)', 'Finance Accounting Tax (FAT)', 'SUPERVISOR FINANCE ACCOUNTING & TAX', 'Admin Finance Accounting & Tax', 'Finance, Accounting & Tax Analyst', 'Finance, Accounting & Tax Staff', 'Staff Finance Accounting & Tax', 'Admin Project and Finance', 'Admin Purchasing & Finance', 'Staff Finance', 'Finance, Accounting, & Tax (FAT) Staf', 'Supervisor Finance Accounting & Tax', 'SPV. Finance, Accounting, Tax', 'Admin Finance, Accounting & Tax', 'Finance, Accounting, Tax Staff', 'Senior Finance Accounting & Tax', 'STAFF FINANCE', 'Staff Finance, Accounting, Tax', 'Finance Accounting & Tax Supervisor', 'Finance Accounting Tax Supervisor', 'Finance Accounting Tax (FAT) Officer', 'FINANCE (ACCOUNTING & TAX)', 'Finance & accounting staff', 'Koordinator Finance, Accounting, Tax', 'Finance, Accounting, Tax Supervisor', 'Administration & Finance Intern', 'Finance, Accounting & Tax Specialist', 'Head of Finance Accounting Tax', 'Staf Finance, Accounting, & Tax', 'HR, ADMIN AND FINANCE INTERNHSIP', 'Chief Finance, Accounting & Tax', 'Bancasurance Finansial Advisor', 'Senior Finance Accounting & Tax Officer', 'Admin Finance, Accounting, Tax', 'Finance Accounting Tax Family', 'FAT (Finance, Accounting & Tax) Supervisor', 'Finance Accounting & Tax Staff', 'FINANCE, ACCOUNTING, TAX STAFF', 'Finance, Accounting & Tax Supervisor', 'Finance, Accounting & Tax Assistant Manager', 'Finance manager', 'Finance Accounting Tax staff', 'Senior Officer Finance, Accounting & Tax', 'Finance', 'Administrasi Finance dan Purchasing', 'staff finance', 'FAT (Finance, Accounting & Tax) Internship', 'Finance Administration - SPD Bandung', 'Finance Internship', 'Finance Administration Staff', 'Finance, Accounting, Tax Manager', 'FINANCE', 'Finance & Accounting Tax (Perusahaan Kapal Tongkang)', 'Finance (Internship)', 'SENIOR FINANCE ACCOUNTING TAX', 'Staff Finance, Accounting, Tax dan Sales', 'Finance Manager', 'Administrasi Sistem Operasi', 'finance', 'Staff Finance, Accounting & Tax', 'SENIOR FINANCE MANAGER', 'FINANCE ACCOUNTING TAX', 'Finance Accounting Tax dan Purchasing', 'Finance Admin (Accounts Payable Intern)', 'Staff FAT (Finance, Accounting, & Tax)', 'Project Finance Manager', 'Junior Finance Officer', 'Staff Finance (accounting)', 'Staff Finance & Accounting', 'Branch Admin (Finance Team)', 'Finance, Accounting & Tax (FAT)', 'Finance Supervisor', 'Finance Accounting Tax Specialist Creative Agency', 'Senior Finance Accounting Tax', 'staff Finance', 'Finance & Accounting', 'Finance Account Payable', 'E-commerce Admin (Finance & Customer Support)', 'Supervisor Finance, Accounting, Tax', 'Finance Supervisor Yayasan', 'Admin Keuangan', 'Finance Accounting & Tax Supervisor (F&B)', 'Finance, Accounting, Tax Officer', 'Supervisor Finance, Accounting & Tax', 'Supervisor Finance', 'Supervisor Finance, Accounting, & Tax', 'Staff Finance Accounting', 'Finance-Accounting & Tax Manager Property Management', 'Staff Finance-AP', 'Finance Intern', 'Accounting & Finance Officer', 'Finance Project', 'Accounting & Finance', 'FAT Staff (Finance, Accounting & Tax Staff)', 'Supervisor Finance, Accounting, Tax MLTI', 'Finance Staff', 'INTERNSHIP FINANCE', 'FAT Manager (Finance, Accounting & Tax Manager)', 'Senior Finance', 'Personal Assistant (Finance Aware)', 'Staf Finance', 'Magang Admin Finance Accounting Tax (FAT)', 'Finance Accounting', 'MANAGER FINANCE ACCOUNTING', 'Finance & Tax', 'Finance Strategist', 'finance accounting', 'Finance  Manager', 'Sales Manager', 'Staff Admin Lapangan Padel', 'Admin Proyek & Sales Support', 'Data Analyst', 'Intern-Data Analyst', 'DATA ANALYST & MONITORING', 'Data Analyst Logistic', 'Data Analyst Intern', 'Marketing Data Analyst', 'Data Analyst Staff', 'IT Data Analyst', 'Staff Data  Analyst', 'Admin Data Analyst', 'Product Data Analyst', 'Senior Data Analyst', 'intern data analyst', 'Business & Data Analyst', 'Data Analyst (Power BI)', 'Admin Marketing & Data Analyst', 'IT System & Data Analyst', 'Data Intelligence Analyst', 'Data Migration Analyst', 'Sales Data Analyst', 'Data Center Analyst', 'Spare Part Data Analyst', 'Dashboard Operations & Data Analyst', 'Real Time Analyst (Data Analyst)', 'Junior Data Analyst', 'Data Analyst (Onsite at Bandung)', 'Data Analyst - Loc: Jakarta Utara', 'Data Manager & Analyst', 'Data Analyst and IT Support', 'Data Analyst (Can join ASAP)', 'Telecom Data Analyst – Crowdsourced Analytic', 'Data Analyst (CRM & Management Lead)', 'Junior Social Media Data Analyst', 'Data Analyst - Cost Management Logistik', 'Marketing Data Analyst (Walk-In Customer)', 'Marketing Data Analyst (Repeat Order Customer)', 'Business Intelligence & Strategic Data Analyst', 'Data Center Analyst (Divisi Marketing)', 'Accounting Data Analyst', 'Data Analyst (Mandarin Speaker - Jkt Timur)', 'Data Analyst (ETL Python Tableau) ASAP - WFO Jakarta', 'Data Analis', 'Staf Analisa Data', 'Middle Data Analysis', 'Functional Analyst', 'Admin Data Analis', 'Statistical Analyst', 'Data Analytic', 'System Analyst', 'Data Scienstist', 'Data & Systems Analyst Intern', 'Data Validator Staff', 'DATA ENTRY', 'Data Entry', 'Data Pipeline', 'Business Analyst', 'Administrasi server analisa data', 'ADMIN ONLINE (WORDPRESS & DATA)', 'Digital Strategist & Analyst', 'Financial System Analyst', 'Data Entry Internship', 'Data Admin', 'Internship System analyst', 'data entry freshgraduate', 'Business System Analyst', 'Freelance Data Entry', 'Internship Data Entry', 'Data Analytics Solution', 'Junior Instruktur Data Analisis', 'Associate Data Entry', 'business analyst', 'Jr. Data Linguist', 'DATA CENTER ANALYS (DIVISI PIUTANG)', 'electronic data processing', 'Marketing Analyst', 'Data Administrator', 'Data Specialist', 'BRAND ANALYST', 'Data Center Analyst (Accounting)', 'Staff Data Control', 'QA System Analyst', 'Lead Business Analyst', 'System Analyst (LARK)', 'System Analyst GRIT', 'Financial Business Analyst', 'IT business analyst', 'Middle Business Analyst', 'Paid Internship - Data Entry', 'Staff Entry Data', 'Senior IT System Analyst', 'Business Analyst (Odoo)', 'Staff Data Entry', 'Accounting Data Entry', 'Admin Data Storage', 'System Analyst – PJP 2', 'Analis Staf', 'FREELANCE DATA ANNOTATOR – AUTODRIVING PROJECT', 'Data Verifier', 'Operator Data Entry', 'ADMIN INPUT DATA', 'Admin Data HRD', 'Security Analyst', 'DATA ENTRY VISA UMROH', 'GIS Analyst', 'Forex Analyst', 'Data Processing Staff', 'CS Admin (Data Entry)', 'Data Analist', 'STAF DATA ANALISIS', 'Social Media Analyst', 'Business Analyst Junior', 'Senior Business Analyst', 'IT BUSINESS ANALYST', 'Admin Data Entry Procurment', 'Analis Bisnis Data', 'Business Analyst- HR', 'Presales Data', 'Technical System Analyst (Project-Based)', 'TEKNISI FIRE SUPRESSION DI DATA CENTER', 'Tier 1 SOC Analyst', 'Data Scientist', 'Business Analyst - General', 'IT Business System Analyst', 'Business Analyst (Insurance Industry', 'Legal Analyst', 'KYC Data Entry English', 'Software Engineer (Intern)', 'Software Engineer (Semarang)', 'Software Engineer Instructor', 'Software Engineer - Intern (Paid Internship)', 'Fullstack Software Engineer', 'Software Engineer (PHP, Javascript)', 'Software QA Engineer', 'Software Engineer (Full Stack)', 'Sr. Full Stack Software Engineer', 'Software Development Manager', 'Software Quality Assurance', 'Software Engineer - Fullstack (Laravel) Intern', 'Graduate Intern - Software Engineer', 'IT Software Engineer .Net 5 above', 'Cloud Engineer Mid Level', 'Data Engineer', 'Junior Software Engineer (Java, Angular) - Prefer ASAP', 'Cloud Engineer', 'engineer confluent kafka', 'Senior Data Engineer', 'data engineer', 'SLACK ENGINEER', 'DATA ENGINEER', 'Software Engineer PM (JAPANESE or MANDARIN Speaker)', 'Data Engineer - Middle Level', 'Cloud Infra Engineer (Junior)', 'Downstream Engineer - Banking Syariah', 'Data Engineer (Freelance)', 'AI Data Engineer', 'Software Tester', 'Machine Learning Engineer', 'Senior Cloud Engineer', 'AI cloud engineer', 'SRE & Devops Engineer', 'QA Engineer Intern', 'Downstream Engineer - Banking (project base)', 'Engineer', 'Business Intelligence Engineer (Multifinance Industry)', 'Technical Support Engineer', 'Tech Engineer', 'Technical Engineer', 'Data Engineer (ETL – Microsoft Fabric) - ASAP', 'Data Engineer (E-Commerce)', 'AI Engineer & Automation Architect', 'Automation Engineer', 'HVAC Engineer', 'IT Compliance & Security Engineer', 'IT Engineer', 'Mechanical Design Engineer', 'BI Engineer', 'AI Software Developer', 'Data Engineer (Cikarang Area)', '(IT) Software Developer', 'Data Engineer (Tableau, ETL) - Financial Industry (ASAP)', 'BI Platform Engineer - Data Dev (Loc: Jakarta Utara)', 'AI Integration & Automation Engineer', 'Data Engineer (Project Based)', 'AI Automation Engineer', 'Marketing Engineer', 'Senior Data Engineer (Project Based)', 'Data Engineer Internship', 'QAQC Automation Engineer', 'QA Automation Engineer', 'Marketing IT (IT Software ERP)', 'engineer', 'Pre-Sales & Data Engineer (Spark Platform)', 'Quality Assurance Software Development', 'Engineer (Magang)', 'Project Engineer HVAC', 'Software Quality Assurance (Senior)', 'Software Quality Assurance (Automation)', 'Software Functional Consultant', 'DevOps Engineer', 'QA Engineer', 'AI Engineer', 'Security Engineer', 'Cybersecurity Engineer', 'Marine Technical Engineer', 'Java Software Developer', 'Testing Engineer', 'Database Engineer', 'Engineer Onsite', 'Fullstack Engineer', 'Network Engineer', 'Technical Engineer WT (Water Treatment)', 'Infrastructure Engineer', 'Design Engineer', 'Systems & Network Automation Engineer', 'Devops Engineer', 'Technical Engineer (Teknisi)', 'System Engineer', 'Robotics Engineer', 'Web Engineer', 'Internship Teknisi Software & Hardware', 'Kubernetes Engineer', 'Technical Support Engineer ( Network & VoIP)', 'Teknik Elektro Tangerang', 'Software Development', 'HVAC Design Engineer', 'Senior Ruby on Rails', 'Sales Engineer (Surabaya)', 'Jr. Scrum Master for Banking Industry', 'Cloud Solution Architect', 'IT Project Coordinator (Software)', 'Solution Architect', 'Solution Architect (Financial Services)', 'Senior IT Solution Architect', 'IT Solution Architect', 'IT software & hardware', 'software sales consultant', 'Sr. Solution Architecture', 'Service Engineer', 'Software Sales Executive', 'Software Product Manager', 'Software Implementation Consultant', 'Field Application Engineer', 'Electrical Engineer', 'Proposal Engineer', 'Sofware AG for Banking Industry', 'Senior Solution Architecture', 'Quality Engineer', 'Senior Engineer', 'Facilities Engineer', 'Equipment Engineer', 'Mechanical Design Engineer (Maritime Technology)', 'GTM Engineer', 'Architect Engineer', 'Application Engineer', 'Structural Engineer', 'Presales Engineer', 'site engineer', 'Chief Engineer', 'Civil Engineer', 'Solution Architecture (Multi finance industry)', 'CIVIL ENGINEER', 'Production Engineer', 'SALES ENGINEER', 'Field Engineer', 'Infrastructure cloud engineer', 'Back-End Engineer', 'Site Reliability Engineer', 'Java Development Engineer', 'Senior Database Engineer', 'IT Software Quality Assurance', 'Fullstack Web Engineer', 'Customer Support Engineer', 'IT Solutions Engineer', 'Internship Presales Engineer', 'System Engineer -  Junior', 'Quality Assurance Engineer', 'digital marketing', 'Digital Marketing Specialist', 'Digital Marketing Strategist', 'Digital Marketing Coordinator', 'Digital Marketing (Advertising)', 'DIGITAL MARKETING', 'Digital Marketing Officer', 'Digital marketing Intern', 'Digital Marketing Intern', 'Digital marketing', 'Digital Marketing Executive', 'Digital marketing specialist', 'Digital Marketing Staff', 'Sales and Digital Marketing', 'Digital Marketing (Strategist)', 'Digital Marketing Communication', 'DIGITAL MARKETING SPECIALIST', 'Digital Marketing (Specialist)', 'Digital Marketing Manager', 'Staf marketing & Digital Marketing', 'Marketing Digital', 'Digital Marketing  Restaurant', 'digital marketing specialist', 'Digital Marketing Supervisor', 'DIGITAL MARKETING STAFF', 'Digital Marketing Internship', 'Digital Marketing Consultant', 'Admin Digital Marketing', 'Digital content & Marketing Specialist', 'SPV Digital Marketing', 'Staff Marketing (Digital Marketing)', 'Mentor Digital Marketing', 'DIGITAL & MARKETING SPESIALIS', 'Digital Marketing Specialist (Bandung)', 'Sales Digital Marketing', '360 Digital Marketing', 'Digital Marketing Lead', 'Digital & Marketing (Koordinator)', 'Event & Digital Marketing', 'Digital Marketing Excecutive', 'Lead Digital Marketing', 'Digital Marketing Associate', 'Customer Service', 'Customer Service Agent', 'Customer Service Staff', 'Customer Service Online', 'customer service', 'Admin Customer Service', 'Admin Customer Service ( CS )', 'CUSTOMER SERVICE ONLINE', 'Admin & Customer Service', 'Customer service online', 'Customer Service Agent -Yogyakarta', 'Customer Service Retail', 'CUSTOMER SERVICE GADAI', 'Customer Service Support', 'ADMIN CUSTOMER SERVICE', 'Customer Service Officer', 'Customer Service Intern', 'Sales & Customer Service Executive', 'Customer Service Representative', 'Admin Customer Service Officer', 'Sr Customer Service', 'Customer Service Offline', 'Customer Service & Sales', 'Customer Service Percetakan', 'Internship - Customer Service', 'Customer Service Pusat', 'Magang Customer Service', 'Customer Service Ekspedisi', 'Customer Service Livechat', 'customer service acquisition', 'Customer Service Acquisition', 'Customer Service Operations', 'Admin & Customer Service E-Commerce', 'Admin Customer Service (Qontak)', 'Customer Service English Speaker', 'Customer Service Admin', 'Customer Service Staff Jogja', 'Customer Service (Freight Forwarding)', 'Customer Service Specialist', 'Customer Service Marketing', 'ADMIN & CUSTOMER SERVICE', 'Customer Service Hotel']


BASE_URL = "http://127.0.0.1:8000"
INFERENSI_URL = f"{BASE_URL}/api/inferensi/"

st.set_page_config(
    page_title="Rekomendasi Loker",
    page_icon="💼",
    layout="wide",
)

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


def extract_text_from_docx(file_bytes: bytes) -> str:
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in doc.paragraphs)


def extract_text(uploaded_file) -> str:
    file_bytes = uploaded_file.read()
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif name.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    elif name.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")
    return ""


# Pendidikan — urutan dari tertinggi ke terendah agar match pertama = paling tinggi
# Nilai DB: "bachelor degree", "high school", "professional certificate",
#           "postgraduate degree", "professional education"
_EDUCATION_MAP = [
    # postgraduate / S2 / S3
    (r"\b(s\.?3|doktor|ph\.?d|doctor)\b",                  "postgraduate degree"),
    (r"\b(s\.?2|magister|master|m\.sc|m\.si|m\.eng)\b",    "postgraduate degree"),
    # professional education
    (r"\b(professional\s+education|pendidikan\s+profesi)\b","professional education"),
    # professional certificate
    (r"\b(professional\s+cert|sertifikat\s+profesi|certified)\b", "professional certificate"),
    # bachelor / S1 / D4
    (r"\b(s\.?1|sarjana|bachelor|b\.sc|b\.eng|d\.?4|diploma\s*iv)\b", "bachelor degree"),
    # high school / SMA / SMK / D1-D3
    (r"\b(d\.?3|diploma\s*(iii|3))\b",                     "high school"),
    (r"\b(d\.?2|diploma\s*(ii|2))\b",                      "high school"),
    (r"\b(d\.?1|diploma\s*(i|1))\b",                       "high school"),
    (r"\b(sma|smk|sekolah\s+menengah|high\s+school)\b",    "high school"),
]

# Tipe — nilai DB: FULL_TIME, CONTRACTOR, INTERN, PART_TIME
_TIPE_MAP = [
    (r"\b(full[\s\-]?time|penuh\s+waktu)\b",               "FULL_TIME"),
    (r"\b(part[\s\-]?time|paruh\s+waktu)\b",               "PART_TIME"),
    (r"\b(intern(ship)?|magang|praktek\s+kerja)\b",        "INTERN"),
    (r"\b(contract(or)?|kontrak|freelance|project\s+based)\b", "CONTRACTOR"),
]

# Industri — nilai DB (top values dari dataset)
_INDUSTRI_MAP = [
    (r"\b(information\s+technology|it\s+service|software\s+house|tech(nology)?)\b",
     "Information Technology and Services"),
    (r"\b(computer\s+software|software\s+development|aplikasi)\b",
     "Computer Software"),
    (r"\b(retail|ritel|toko|e[\-\s]?commerce|marketplace)\b",
     "Retail"),
    (r"\b(marketing|advertising|iklan|promosi|digital\s+marketing)\b",
     "Marketing and Advertising"),
    (r"\b(food|beverage|fnb|f&b|makanan|minuman|restoran|kuliner)\b",
     "Food & Beverages"),
    (r"\b(fashion|apparel|garment|pakaian|tekstil)\b",
     "Apparel & Fashion"),
    (r"\b(manufactur|pabrik|produksi|industri\s+manufaktur)\b",
     "Manufacturing"),
    (r"\b(automotive|otomotif|kendaraan|mobil|motor)\b",
     "Automotive"),
    (r"\b(education|pendidikan|sekolah|universitas|kampus|training)\b",
     "Education Management"),
    (r"\b(health|wellness|fitness|kesehatan|medis|klinik|rumah\s+sakit)\b",
     "Health, Wellness and Fitness"),
    (r"\b(human\s+resource|hr|sdm|rekrutmen|staffing)\b",
     "Human Resources"),
    (r"\b(construction|konstruksi|bangunan|properti|real\s+estate)\b",
     "Construction"),
    (r"\b(outsourc|offshoring|bpo)\b",
     "Outsourcing/Offshoring"),
    (r"\b(logistic|supply\s+chain|ekspedisi|pengiriman|warehouse)\b",
     "Logistics and Supply Chain"),
    (r"\b(consumer\s+service|layanan\s+pelanggan|customer\s+service)\b",
     "Consumer Services"),
    (r"\b(financial\s+service|keuangan|perbankan|bank|asuransi|insurance|fintech)\b",
     "Financial Services"),
    (r"\b(management\s+consult|konsultan\s+manajemen)\b",
     "Management Consulting"),
    (r"\b(consumer\s+goods|fmcg|barang\s+konsumsi)\b",
     "Consumer Goods"),
]

# Kategori — nilai DB (top values dari dataset)
_KATEGORI_MAP = [
    (r"\b(admin(istrat)?|tata\s+usaha|office\s+admin|staff\s+admin)\b",
     "Administrative Staff"),
    (r"\b(digital\s+marketing|social\s+media|seo|sem|content\s+marketing)\b",
     "Digital Marketing Specialist"),
    (r"\b(customer\s+service|cs|layanan\s+pelanggan|call\s+center)\b",
     "Customer Service Representative"),
    (r"\b(backend|back[\s\-]end|back\s+end|api\s+developer|server[\s\-]side)\b",
     "Backend Developer"),
    (r"\b(full[\s\-]?stack|fullstack)\b",
     "Full Stack Developer"),
    (r"\b(frontend|front[\s\-]end|front\s+end|ui\s+developer|react|vue|angular)\b",
     "Frontend Developer"),
    (r"\b(graphic\s+design|desain\s+grafis|visual\s+design|brand\s+design)\b",
     "Desainer Grafis & Brand"),
    (r"\b(video\s+edit|film\s+edit|editor\s+video|motion\s+graphic)\b",
     "Film & Video Editor"),
    (r"\b(data\s+analyst|analisis\s+data|business\s+intelligence|bi\s+analyst)\b",
     "Data Analyst"),
    (r"\b(accountant|akuntan|akuntansi|accounting)\b",
     "Accountant"),
    (r"\b(tax|pajak|perpajakan)\b",
     "Tax Accountant"),
    (r"\b(data\s+engineer|etl|data\s+pipeline|data\s+warehouse)\b",
     "Data Engineer"),
    (r"\b(system\s+analyst|analisis\s+sistem|business\s+analyst)\b",
     "System Analyst"),
    (r"\b(finance\s+manager|manajer\s+keuangan|kepala\s+keuangan)\b",
     "Finance Manager"),
    (r"\b(sales\s+rep|sales\s+executive|tenaga\s+penjual)\b",
     "Sales Representative"),
    (r"\b(mobile\s+dev|android|ios\s+dev|flutter|react\s+native)\b",
     "Mobile Developer"),
    (r"\b(devops|site\s+reliability|sre|cloud\s+engineer|infrastructure)\b",
     "Devops Engineer"),
    (r"\b(qa|quality\s+assurance|tester|testing|software\s+test)\b",
     "QA Engineer"),
    (r"\b(data\s+scientist|machine\s+learning|ml\s+engineer|deep\s+learning|ai\s+engineer)\b",
     "Data Analyst"),  # closest match di DB
    (r"\b(software\s+architect|solution\s+architect|enterprise\s+architect)\b",
     "Software Architect"),
    (r"\b(content\s+creator|youtuber|influencer|kreator\s+konten)\b",
     "Content Creator"),
    (r"\b(finance\s+staff|staf\s+keuangan|finance\s+officer)\b",
     "Finance Staff"),
    (r"\b(technical\s+support|it\s+support|helpdesk|support\s+engineer)\b",
     "Technical Support Engineer"),
    (r"\b(sales\s+operat|sales\s+admin|koordinator\s+sales)\b",
     "Sales Operations"),
    (r"\b(data\s+entry|input\s+data|operator\s+data)\b",
     "Data Entry Clerk"),
    (r"\b(editor|penulis|copywriter|content\s+writer|journalist)\b",
     "Editor"),
    (r"\b(videographer|kameraman|photographer|fotografer)\b",
     "Videographer"),
    (r"\b(fashion\s+design|desainer\s+busana|desainer\s+mode)\b",
     "Fashion Designer"),
    (r"\b(interior\s+design|desainer\s+interior|arsitektur\s+interior)\b",
     "Desainer Interior"),
    (r"\b(sales\s+promot|promotor|spg|spb)\b",
     "Sales Promoter"),
]

_SKILLS_SECTION_HEADERS = [
    r"skills?", r"keahlian", r"kemampuan", r"kompetensi",
    r"technical\s+skills?", r"hard\s+skills?", r"soft\s+skills?",
    r"tools?", r"technologies?", r"teknologi", r"keterampilan",
]

_TITLE_SECTION_HEADERS = [
    r"posisi\s+yang\s+dilamar", r"position\s+applied", r"desired\s+position",
    r"objective", r"summary", r"profil", r"profile",
    r"career\s+objective", r"tujuan\s+karir", r"ringkasan",
]


def _find_section(text: str, headers: list, max_lines: int = 8) -> str:
    """Cari section berdasarkan header, ambil beberapa baris setelahnya."""
    pattern = (
        r"(?i)(?:^|\n)\s*(?:" + "|".join(headers) + r")\s*[:\-]?\s*\n"
        r"((?:.+\n?){1," + str(max_lines) + r"})"
    )
    m = re.search(pattern, text)
    if m:
        return m.group(1).strip()
    return ""


def _match_first(text_lower: str, mapping: list) -> str:
    """Return label dari pattern pertama yang cocok."""
    for pattern, label in mapping:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return label
    return ""


def _best_match_from_arr(text_lower: str, arr: list) -> str:
    """Cari item dari arr yang paling banyak kata-katanya muncul di text."""
    best, best_score = "", 0
    for item in arr:
        if item in ("Tidak ada", ""):
            continue
        words = re.findall(r"\w+", item.lower())
        score = sum(1 for w in words if re.search(r"\b" + re.escape(w) + r"\b", text_lower))
        if score > best_score:
            best_score = score
            best = item
    return best if best_score > 0 else ""


def _match_skills_from_arr(text: str, arr: list) -> str:
    """Cari semua skill dari arr yang muncul di teks CV."""
    text_lower = text.lower()
    found = []
    for skill in arr:
        if skill in ("Tidak ada", ""):
            continue
        if re.search(r"\b" + re.escape(skill.lower()) + r"\b", text_lower):
            found.append(skill)
    return ", ".join(found[:20])


def parse_cv_fields(text: str) -> dict:
    text_lower = text.lower()

    # ── Pendidikan ──
    pendidikan = _match_first(text_lower, _EDUCATION_MAP)

    # ── Tipe ──
    tipe = _match_first(text_lower, _TIPE_MAP)

    # ── Industri — pakai industri_arr ──
    industri = _best_match_from_arr(text_lower, industri_arr)
    if not industri:
        industri = _match_first(text_lower, _INDUSTRI_MAP)

    # ── Skills — pakai skill_arr ──
    skills_clean = _match_skills_from_arr(text, skill_arr)
    if not skills_clean:
        skills_raw = _find_section(text, _SKILLS_SECTION_HEADERS, max_lines=10)
        if not skills_raw:
            skill_lines = [
                line.strip()
                for line in text.splitlines()
                if line.count(",") >= 2 and len(line.strip()) < 200
            ]
            skills_raw = ", ".join(skill_lines[:3])
        skills_clean = re.sub(r"[•\-\*▪►\n]", ", ", skills_raw)
        skills_clean = re.sub(r",\s*,+", ",", skills_clean)
        skills_clean = re.sub(r"\s*,\s*", ", ", skills_clean).strip(", ")

    # ── Judul / Posisi — pakai judul_arr ──
    title = ""
    title_section = _find_section(text, _TITLE_SECTION_HEADERS, max_lines=2)
    if title_section:
        title = title_section.splitlines()[0].strip()
    title_from_arr = _best_match_from_arr(text_lower[:500], judul_arr)
    if title_from_arr and (not title or len(title_from_arr) > 3):
        title = title_from_arr
    if not title:
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        if len(lines) >= 2:
            title = lines[1]

    # ── Kategori — pakai kategori_arr ──
    combined = (title + " " + text[:500]).lower()
    kategori = _best_match_from_arr(combined, kategori_arr)
    if not kategori:
        kategori = _match_first(combined, _KATEGORI_MAP)

    return {
        "title": title[:100],
        "industri": industri,
        "kategori": kategori,
        "pendidikan": pendidikan,
        "tipe": tipe,
        "skills": skills_clean[:500],
    }


st.title("Sistem Rekomendasi Lowongan Kerja")
st.markdown(
    "Upload CV kamu (PDF, DOCX, atau TXT) — sistem akan otomatis mengekstrak "
    "informasi dan mencarikan lowongan yang paling cocok."
)
st.divider()

uploaded_file = st.file_uploader(
    "Upload CV kamu",
    type=["pdf", "docx", "txt"],
    help="Format yang didukung: PDF, DOCX, TXT",
)

if uploaded_file is None:
    st.info("Upload CV untuk memulai pencarian.")
    st.stop()

# Ekstrak & parse
with st.spinner("Membaca dan menganalisis CV..."):
    cv_text = extract_text(uploaded_file)
    fields = parse_cv_fields(cv_text)

st.success(f"CV berhasil dibaca ({len(cv_text)} karakter)")

with st.expander("Lihat teks mentah CV"):
    st.text(cv_text[:3000] + ("..." if len(cv_text) > 3000 else ""))

# Tampilkan hasil ekstraksi (read-only)
with st.expander("Hasil ekstraksi CV", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Posisi:** {fields['title'] or '-'}")
        st.markdown(f"**Industri:** {fields['industri'] or '-'}")
        st.markdown(f"**Kategori:** {fields['kategori'] or '-'}")
    with c2:
        st.markdown(f"**Pendidikan:** {fields['pendidikan'] or '-'}")
        st.markdown(f"**Tipe:** {fields['tipe'] or '-'}")
    st.markdown(f"**Skills:** {fields['skills'] or '-'}")

st.divider()

# Validasi & kirim ke API
if not fields["title"]:
    st.warning("Posisi tidak terdeteksi dari CV. Pastikan CV memuat judul posisi yang jelas.")
    st.stop()

payload = {
    "title":      fields["title"],
    "industri":   fields["industri"],
    "kategori":   fields["kategori"],
    "pendidikan": fields["pendidikan"],
    "tipe":       fields["tipe"],
    "skills":     fields["skills"],
}

with st.spinner("Sedang menganalisis kecocokan dengan semua lowongan..."):
    try:
        response = requests.post(INFERENSI_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.ConnectionError:
        st.error(
            "Tidak bisa terhubung ke server Django. "
            "Pastikan server sudah berjalan di http://127.0.0.1:8000"
        )
        st.stop()
    except requests.exceptions.Timeout:
        st.error("Request timeout. Server terlalu lama merespons.")
        st.stop()
    except requests.exceptions.HTTPError as e:
        err_msg = response.json().get("error", str(e))
        st.error(f"Error dari server: {err_msg}")
        st.stop()
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        st.stop()

rekomendasi = data.get("rekomendasi", [])
total = data.get("total_lowongan_dianalisis", 0)

st.subheader("Hasil Rekomendasi")
st.success(
    f"Berhasil menganalisis **{total}** lowongan. "
    f"Menampilkan **{len(rekomendasi)}** rekomendasi terbaik."
)

if not rekomendasi:
    st.info("Tidak ada rekomendasi yang ditemukan.")
    st.stop()

for item in rekomendasi:
    ranking = item.get("ranking", "-")
    skor    = item.get("skor_kecocokan", 0)
    loker   = item.get("detail_loker", {})

    judul       = loker.get("judul") or "Tanpa Judul"
    perusahaan  = loker.get("perusahaan") or "Perusahaan tidak diketahui"
    kota        = loker.get("kota") or ""
    provinsi    = loker.get("provinsi") or ""
    lokasi      = ", ".join(filter(None, [kota, provinsi])) or "Lokasi tidak tersedia"
    tipe_loker  = loker.get("tipe") or "-"
    ind_loker   = loker.get("industri") or "-"
    kat_loker   = loker.get("kategori") or "-"
    pend_loker  = loker.get("pendidikan") or "-"
    skill_loker = loker.get("skills") or "-"
    gaji_min    = loker.get("gaji_min") or ""
    gaji_max    = loker.get("gaji_max") or ""
    gaji_cur    = loker.get("gaji_currency") or ""
    gaji_unit   = loker.get("gaji_unit") or ""
    link        = loker.get("link") or ""
    deskripsi   = loker.get("deskripsi") or ""
    benefit     = loker.get("benefit") or ""

    if gaji_min and gaji_max:
        gaji_str = f"{gaji_cur} {gaji_min} - {gaji_max} / {gaji_unit}"
    elif gaji_min:
        gaji_str = f"{gaji_cur} {gaji_min} / {gaji_unit}"
    else:
        gaji_str = "Tidak disebutkan"

    badge = "Tinggi" if skor >= 0.7 else ("Sedang" if skor >= 0.4 else "Rendah")

    with st.container(border=True):
        header_col, skor_col = st.columns([4, 1])
        with header_col:
            st.markdown(f"### #{ranking} - {judul}")
            st.markdown(f"**{perusahaan}** | {lokasi}")
        with skor_col:
            st.metric(label="Skor Kecocokan", value=f"{skor:.2%}", delta=badge)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"**Tipe:** {tipe_loker}")
            st.markdown(f"**Industri:** {ind_loker}")
        with c2:
            st.markdown(f"**Kategori:** {kat_loker}")
            st.markdown(f"**Pendidikan:** {pend_loker}")
        with c3:
            st.markdown(f"**Gaji:** {gaji_str}")

        st.markdown(f"**Skills:** {skill_loker}")

        if deskripsi or benefit:
            with st.expander("Lihat Deskripsi & Benefit"):
                if deskripsi:
                    st.markdown("**Deskripsi Pekerjaan:**")
                    st.write(deskripsi)
                if benefit:
                    st.markdown("**Benefit:**")
                    st.write(benefit)

        if link:
            st.link_button("Lamar Sekarang", url=link)

    st.write("")
