import itertools
import dataclasses
import typing
import typeguard
import numpy as np
import scipy.ndimage

# typing
Scaler3D = typing.Tuple[int, int, int]


# https://en.wikipedia.org/wiki/Rotation_matrix
# Rx = [[      1,      0,      0],
#       [      0,  cos(), -sin()],
#       [      0,  sin(),  cos()]]
# Ry = [[  cos(),      0,  sin()],
#       [      0,      1,      0],
#       [ -sin(),      0,  cos()]]
# Rz = [[  cos(), -sin(),      0],
#       [  sin(),  cos(),      0],
#       [      0,      0,      1]]
ROT90_X = np.array(
    [[ 1,  0,  0],
     [ 0,  0, -1],
     [ 0,  1,  0]])
ROT90_Y = np.array(
    [[ 0,  0,  1],
     [ 0,  1,  0],
     [-1,  0,  0]])
ROT90_Z = np.array(
    [[ 0, -1 , 0],
     [ 1,  0,  0],
     [ 0,  0,  1]])


@dataclasses.dataclass
class VolumeBrick:
    brick: 'Brick'
    volume: np.ndarray


@typeguard.typechecked
def vol2pts(volume: np.ndarray) -> np.ndarray:
    return np.array([p for p in zip(*np.where(volume == 1))], dtype=np.int8)


@typeguard.typechecked
class Brick():
    def __init__(self,
            points: np.ndarray,
            color: str='gray',
            rotate: Scaler3D=(0, 0, 0),
            offset: Scaler3D=(0, 0, 0)):
        if not isinstance(points, np.ndarray):
            raise NotImplementedError('points not a ndarray')
        if len(points.shape) not in [2]:
            raise ValueError('points not a 2-d ndarray')
        if points.shape[1] not in [3]:
            raise ValueError('points not a 2-d of 3d points ndarray')
        self._points = points.astype(np.int8)
        # TODO: check color, rotate, offset
        self._color = color
        self._rotate = rotate
        self._offset = offset

    def __repr__(self) -> str:
        return (
            f'Brick({self.color}): {self.count} points'
            f' rotate {self.rotate} offset {self.offset}')

    @property
    def color(self) -> str:
        return self._color

    @property
    def rotate(self) -> Scaler3D:
        return self._rotate

    @property
    def offset(self) -> Scaler3D:
        return self._offset

    @property
    def count(self) -> int:
        ''' returns number of points '''
        return len(self._points)

    @property
    def points(self) -> np.ndarray:
        ''' returns absolute points with self.offset and self.rotate '''
        cur_points = self._points
        for ri, rot in enumerate([ROT90_X, ROT90_Y, ROT90_Z]):
            for rt in range(self.rotate[ri]):
                cur_points = cur_points.dot(rot)
        cur_points -= cur_points.min(axis=0)
        cur_points += self.offset
        return cur_points.astype(np.int8)

    def volume(self, shape: Scaler3D=None) -> np.ndarray:
        '''
        returns volume of points with self.offset and self.rotate
        '''
        if shape is None:
            shape = (self.points.max(axis=0) + 1).tolist()
        npy = np.zeros(shape, dtype=np.int8)
        for p in self.points.tolist():
            npy[p[0], p[1], p[2]] = 1
        return npy

    def replica(self, color=None, rotate=None, offset=None) -> 'Brick':
        ''' returns a new brick with rotate and offset '''
        color = self._color if color is None else color
        rotate = self._rotate if rotate is None else rotate
        offset = self._offset if offset is None else offset
        return Brick(self._points, color=color, rotate=rotate, offset=offset)

    def possible(self,
            volume: np.ndarray,
            paddings: typing.Tuple[int, int, int]=(3, 3, 3)
        ) -> typing.List[VolumeBrick]:
        '''
        get all possible replicas in volume.shape + paddings
        returns: VolumeBricks
        '''

        kernel = k = np.array([
                [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
                [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
                [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
            ], dtype=np.int8)

        if len(volume.shape) not in [3] or len(paddings) not in [3]:
            raise ValueError('not a 3d volume shape')
        padded_shape = [s + p for s,p in zip(volume.shape, paddings)]
        padded_volume = np.zeros(padded_shape, dtype=np.int8)
        for p in vol2pts(volume):
            padded_volume[p[0], p[1], p[2]] = 1

        ranges = [[r for r in range(s)] for s in volume.shape]
        volbricks = []
        for rots in itertools.product([s for s in range(4)], repeat=3):
            for ofsts in itertools.product(*ranges):
                brick = self.replica(rotate=rots, offset=ofsts)
                vol = np.zeros(padded_shape, dtype=np.int8)
                for p in brick.points.tolist():
                    vol[p[0], p[1], p[2]] = 1
                left_vol = padded_volume - vol
                # filter out brick not in vol
                if left_vol.min() < 0:
                    continue
                # also filter out which contains any isolated point
                convs = scipy.ndimage.convolve(
                        left_vol, kernel, mode='constant', cval=0)
                if np.count_nonzero(
                        np.logical_and(left_vol > 0, convs == 0)) > 0:
                    continue

                # now it is safe to return in volume.shape
                nvol = np.zeros(volume.shape, dtype=np.int8)
                for p in brick.points.tolist():
                    nvol[p[0], p[1], p[2]] = 1

                volbricks.append(VolumeBrick(brick, nvol))

        # sort points
        unique_sorted_pts = []
        unique_volbricks = []
        for vb in volbricks:
            kpts = sorted(vb.brick.points.tolist())
            if kpts in unique_sorted_pts:
                continue
            unique_sorted_pts.append(kpts)
            unique_volbricks.append(vb)
        return unique_volbricks

    # def possible(self, volume, paddings=3):
        # ''' generator to all possible replicas '''
        # if len(volume.shape) not in [3]:
            # raise ValueError('not a 3d volume shape')
        # ranges = [[r for r in range(s + paddings)] for s in volume.shape]
        # bricks = []
        # for rots in itertools.product([s for s in range(4)], repeat=3):
            # for ofsts in itertools.product(*ranges):
                # bricks.append(self.replica(rotate=rots, offset=ofsts))
        # return bricks


    # def __call__(self, volume):
        # ''' generator to all possible replicas '''
        # if len(volume.shape) not in [3]:
            # raise ValueError('not a 3d volume shape')
        # points = np.array([p for p in zip(*np.where(volume == 1))])
        # ranges = [[r for r in range(s, e + 1)]
                  # for s, e in zip(points.min(axis=0), points.max(axis=0))]
        # for rots in itertools.product([s for s in range(4)], repeat=3):
            # for ofsts in itertools.product(*ranges):
                # # print(f'__call__: rots {rots}, ofsts {ofsts}')
                # yield self.replica(rotate=rots, offset=ofsts)

    # def fit(self, volume):
        # ''' returns list of all possible bricks '''
        # if len(volume.shape) not in [3]:
            # raise ValueError('not a 3d volume shape')
        # points = np.array([p for p in zip(*np.where(volume == 1))])
        # ranges = [[r for r in range(s, e + 1)]
                  # for s, e in zip(points.min(axis=0), points.max(axis=0))]

        # bricks = []
        # for rots in itertools.product([s for s in range(4)], repeat=3):
            # for ofsts in itertools.product(*ranges):
                # bricks.append(self.replica(rotate=rots, offset=ofsts))
        # return bricks
