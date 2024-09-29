from flask import Flask, render_template, request, jsonify, make_response

app = Flask(__name__)


communities = [
    {
        "id": 1,
        "slug": "svelte",
        "title": "Svelte Community",
        "desc": "The Svelte Community brings together developers passionate about Svelte, a modern framework for building fast web applications with minimal code. Engage with fellow enthusiasts, share projects, and learn the latest techniques to make the most out of Svelte's innovative approach to reactive programming.",
        "img": "static/img/svelte.png",
        "members": 500,
        "is_member": True
    },
    {
        "id": 2,
        "slug": "vue",
        "title": "Vue.js Community",
        "desc": "The Vue.js Community is a hub for developers working with Vue.js, one of the most flexible JavaScript frameworks. Join fellow Vue users in discussions, tutorials, and project showcases, and stay connected to the latest updates and best practices within the vibrant Vue ecosystem.",
        "img": "static/img/vue.png",
        "members": 100,
        "is_member": False
    },
    {
        "id": 3,
        "slug": "htmx",
        "title": "HTMX Community",
        "desc": "The HTMX Community is the place for developers exploring how to build modern web interfaces with minimal JavaScript. Here, you can learn how to leverage HTML attributes and server-driven interactions to create rich, responsive UIs without the complexity of traditional front-end frameworks.",
        "img": "static/img/htmx.png",
        "members": 300,
        "is_member": True
    },
    {
        "id": 4,
        "slug": "jquery",
        "title": "jQuery Community",
        "desc": "The jQuery Community remains active with developers who continue to support and use one of the most popular JavaScript libraries ever created. Whether working on legacy projects or new development, this community provides insights, updates, and resources to keep jQuery alive and relevant.",
        "img": "static/img/jquery.png",
        "members": 200,
        "is_member": False
    },
    {
        "id": 5,
        "slug": "react",
        "title": "React Community",
        "desc": "The React Community is where developers gather to discuss all things React.js, from building dynamic user interfaces to exploring the latest features like hooks and concurrent rendering. With numerous resources and a strong following, it's a go-to place for anyone looking to excel in React development.",
        "img": "static/img/react.png",
        "members": 200,
        "is_member": True
    },
    {
        "id": 6,
        "slug": "angular",
        "title": "Angular Community",
        "desc": "The Angular Community is dedicated to developers working with the Angular framework. This is the perfect place for those building complex, large-scale web applications to share ideas, collaborate, and learn about the latest features, tools, and best practices in the Angular ecosystem.",
        "img": "static/img/angular.png",
        "members": 150,
        "is_member": False
    },
    {
        "id": 7,
        "slug": "typescript",
        "title": "TypeScript Community",
        "desc": "The TypeScript Community gathers developers who use TypeScript for writing safer and more scalable JavaScript. Whether you're a newcomer or an experienced TypeScript user, this community offers valuable resources, discussions, and opportunities to dive deeper into this powerful superset of JavaScript.",
        "img": "static/img/typescript.png",
        "members": 600,
        "is_member": True
    },
    {
        "id": 8,
        "slug": "alpinejs",
        "title": "Alpine.js Community",
        "desc": "The Alpine.js Community is a home for developers who enjoy using lightweight, declarative JavaScript for building reactive user interfaces. Here, you can share tips, best practices, and code snippets while learning how Alpine.js can simplify front-end development without the need for complex toolchains.",
        "img": "static/img/alpine.png",
        "members": 400,
        "is_member": True
    },
    {
        "id": 9,
        "slug": "solidjs",
        "title": "Solid.js Community",
        "desc": "The Solid.js Community brings together developers interested in a highly efficient and reactive framework for building web applications. Solid.js offers fine-grained reactivity with exceptional performance, and this community is the place to explore its full potential and discuss real-world use cases.",
        "img": "static/img/solid.png",
        "members": 250,
        "is_member": False
    },
    {
        "id": 10,
        "slug": "inertiajs",
        "title": "Inertia.js Community",
        "desc": "The Inertia.js Community is dedicated to developers building modern monolithic web applications by seamlessly connecting backend frameworks with JavaScript-powered front-ends. Inertia.js simplifies full-stack development, and this community is the ideal place to discuss its use in real-world projects.",
        "img": "static/img/inertia.png",
        "members": 350,
        "is_member": True
    }
]



COMMUNITIES_PER_PAGE = 4

@app.route('/')
def index():
    page = int(request.args.get('page', 1))
    start = (page - 1) * COMMUNITIES_PER_PAGE
    end = start + COMMUNITIES_PER_PAGE
    paginated_communities = communities[start:end]
    total_pages = (len(communities) + COMMUNITIES_PER_PAGE - 1) // COMMUNITIES_PER_PAGE
    
    return render_template(
        'components/pages/index.html', 
        communities=paginated_communities, 
        page=page, 
        total_pages=total_pages
    )

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('search', '').lower()
    filtered_communities = [c for c in communities if query in c['title'].lower()]
    page = int(request.args.get('page', 1))
    start = (page - 1) * COMMUNITIES_PER_PAGE
    end = start + COMMUNITIES_PER_PAGE
    paginated_communities = filtered_communities[start:end]
    total_pages = (len(filtered_communities) + COMMUNITIES_PER_PAGE - 1) // COMMUNITIES_PER_PAGE
    
    return render_template(
        'components/pages/index.html', 
        communities=paginated_communities, 
        page=page, 
        total_pages=total_pages
    )


@app.route('/community/<slug>')
def community(slug):
    community_info = next((c for c in communities if c['slug'] == slug), None)
    if not community_info:
        return "404 - Community not found"
    response = make_response(render_template('components/pages/single.html', community=community_info))
    response.headers['HX-Trigger'] = 'newContact'
    return response


@app.route('/toggle-joing/<int:community_id>', methods=['POST'])
def toggle_community(community_id):
    action = request.args.get('action', 'join')
    community = next((c for c in communities if c['id'] == community_id), None)
    if community:
        if action == 'join':
            community['members'] += 1
            community['is_member'] = True
        elif action == 'unjoin':
            community['members'] -= 1
            community['is_member'] = False
        if request.referrer and '/community' in request.referrer:
            return render_template('components/verticalCard.html', community=community, goback=True)
        else:
            return render_template('components/horizontalCard.html', community=community, goback=False)

if __name__ == '__main__':
    app.run(debug=True)
