import json

from app.main import bp
from app.models import Hieroglyph

from flask import render_template, request, current_app, url_for
from flask_login import login_required


def create_model_generator(model):
    for i, h in enumerate(model):
        model[i].onyomi = ', '.join(json.loads(h.onyomi))
        model[i].kunyomi = ', '.join(json.loads(h.kunyomi))
        model[i].translation = ', '.join(json.loads(h.translation))
    model_gen = ((model[n: n + 4], model[n:])[n + 4 > len(model)] for n in range(0, len(model), 4))
    return model_gen


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    model = Hieroglyph.query.filter_by(level=1).paginate(page, current_app.config['HIEROGLYPHS_PER_PAGE'])
    next_url = (None, url_for('main.index', page=model.next_num))[model.has_next]
    prev_url = (None, url_for('main.index', page=model.prev_num))[model.has_prev]
    return render_template('main/index.html', model=create_model_generator(model.items),
                           next_page=next_url, prev_page=prev_url)