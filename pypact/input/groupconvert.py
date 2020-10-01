class Edge:
    def __init__(self, lower, upper):
        assert upper >= lower
        self.lower = lower
        self.upper = upper

    def get_overlap(self, edge):
        IS_LOWER, IS_UPPER = True, False
        points = sorted([(self.lower, IS_LOWER), (self.upper, IS_UPPER),
                         (edge.lower, IS_LOWER), (edge.upper, IS_UPPER)], key=lambda x: x[0])
        # the second item must be a lower point and the third item must be an upper point
        # for overlap
        overlap = points[1][1] == IS_LOWER and points[2][1] == IS_UPPER
        overlap_width = points[2][0] - points[1][0]

        return overlap, overlap_width

    @property
    def length(self):
        return (self.upper - self.lower)


def _get_edges_from_bounds(bounds):
    return [Edge(bound, bounds[i+1])
            for i, bound in enumerate(bounds[:-1])]


def by_energy(input_bounds, input_values, output_bounds):
    """
        Returns the output_values by simple weighting and sharing
        of bins

        output_bounds is a list of energies, units are irrelevant,
        as long as it matches the units of the input_bounds.

        Asserts both input and output bounds are of length greater than 1

        Assumes that input and output bounds are in ascending energy. If not
        then it will go unchecked and will produce odd results
    """

    assert len(output_bounds) > 1
    assert len(input_bounds) > 1

    input_edges = _get_edges_from_bounds(input_bounds)
    output_edges = _get_edges_from_bounds(output_bounds)

    # this should be exposed as a function arg to allow custom metrics
    # by lethargy for example
    def compute(input_width, input_value, overlapping_width):
        return overlapping_width*input_value/input_width

    def overlaps_and_compute(oedge, last_overlap_index=0):
        output_value = 0.0
        prev_has_overlap = False
        for i, iedge in enumerate(input_edges):
            has_overlap, overlap_width = iedge.get_overlap(oedge)
            if has_overlap:
                # keep track of last overlap index for to avoid starting at 0 each time
                last_overlap_index = i
                output_value += compute(iedge.length,
                                        input_values[i], overlap_width)

            # break early to avoid continuing iteration
            if not has_overlap and prev_has_overlap:
                break

            # we cannot have 2 overlaping adjacent output bounds
            # so return the last index of the input to start at next time
            prev_has_overlap = has_overlap

        return output_value, last_overlap_index

    last_index = 0
    output_values = []
    for edge in output_edges:
        output_value, last_index = overlaps_and_compute(
            edge, last_overlap_index=last_index)
        output_values.append(output_value)

    return output_values
