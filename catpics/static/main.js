var myApp = angular.module('catpics', []);
console.log('HERE')

myApp.controller('CatPicsController', ['$scope', '$log', '$http', function($scope, $log, $http) {
  $log.log('HERE');
  function get_picture(){
    $http.get('/api/random').
      success(function(data, status, headers, config) {
        $log.log(data);
        $scope.image= data['image'];
      }).error(function(error) {
        $log.log(error);
      });
  };
  get_picture();
  setInterval(function(){get_picture()}, 30000);
}]);
