import time
import datetime
from collections import namedtuple
import random

Photo = namedtuple('Photo', ["id", "num_tags", "tags"])

def output(slides, problem):
    with open(problem, "w") as out:
        total_slides = len(slides)
        out.write(str(total_slides) + "\n")
        for i, id in enumerate(slides):
            if i == total_slides - 1:
                out.write(str(id))
            else:
                out.write(str(id) + "\n")


def compute_score(photo1: Photo, photo2: Photo):
    metric1 = len(photo1.tags.intersection(photo2.tags))
    metric2 = len(photo1.tags) - metric1
    metric3 = len(photo2.tags) - metric1
    return min(metric1, metric2, metric3)


def compute_vertical_intersection(photo1: Photo, photo2: Photo):
    return len(photo1.tags.intersection(photo2.tags))


def by_tag_len(photo):
    return photo.num_tags


def build_h_photo(photo1: Photo, photo2: Photo):
    id1 = photo1.id
    id2 = photo2.id
    set_tags = (photo1.tags).union(photo2.tags)
    n_tags = len(set_tags)
    set_id = id1 + " " + id2
    photo_tuple = (set_id, int(n_tags), set(set_tags))
    return Photo(*photo_tuple)


def run(fichero):
    tot_photos = []
    h_photos = []
    v_photos = []
    slides = []
    # Parse photos from file and create list with horizontal and vertical photos
    print("python main function")
    with open(fichero) as f:
        tot = int(f.readline().strip())
        for i, val in enumerate(f.readlines()):
            features = val.split(" ")
            ori = features.pop(0)
            tags = features.pop(0)
            list_tags = []
            for j in features:
                list_tags.append(j.strip())
            photo_tuple = (str(i), int(tags), set(list_tags))
            photo_example = Photo(*photo_tuple)
            tot_photos.append(photo_example)
            if ori == "H":
                h_photos.append(photo_example)
            else:
                v_photos.append(photo_example)

    # Process vertical photos to joint side by side
    while (len(v_photos) > 0):
        pivot = v_photos.pop()
        if (len(v_photos) == 1):
            last_v_photo = v_photos.pop()
            if (compute_vertical_intersection(pivot, last_v_photo) >= 1):
                photo_new = build_h_photo(pivot, last_v_photo)
                h_photos.append(photo_new)
        intersect_score = 9999999
        best_candidate_index = -1
        for index, candidate in enumerate(v_photos):
            score = compute_vertical_intersection(pivot, candidate)
            if score < intersect_score:
                intersect_score = score
                best_candidate_index = index
        if best_candidate_index != -1:
            selected_candidate = v_photos.pop(best_candidate_index)
            photo_new = build_h_photo(pivot, selected_candidate)
            h_photos.append(photo_new)

    # h_aux = h_photos.copy()
    # for i in range(len(h_photos)):
    #     h_photos = h_aux.copy()
        # Process horizontal photos to create a slide
    h_photos.sort(key=by_tag_len)
    # random.shuffle(h_photos)
    pivot = h_photos.pop(   )
    slides.append(pivot.id)
    while (len(h_photos) > 0):
        if(len(h_photos)%500 == 0):
            print(len(h_photos))
        intersect_score = -1
        best_candidate_index = -1
        for index, candidate in enumerate(h_photos):
            score = compute_score(pivot, candidate)
            if intersect_score < score:
                intersect_score = score
                best_candidate_index = index

        if best_candidate_index != -1:
            pivot = h_photos.pop(best_candidate_index)
            slides.append(pivot.id)
    output(slides, "output_" + fichero + str(i) + ".txt")



if __name__ == '__main__':
    start_time = time.time()
    # run("b_lovely_landscapes.txt")
    run("c_memorable_moments.txt")
    # run("d_pet_pictures.txt")
    # run("e_shiny_selfies.txt")
    print("--- %s ---" % str(datetime.timedelta((time.time() - start_time))))
