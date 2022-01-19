if exist('Steeing_Shaft_Torque','var') == 1
    data = Steering_Shaft_Torque.Value
end

histogram(data)
grid on
xlim([-50,50])
line([5,5], ylim, 'LineWidth', 2, 'Color', 'r');
line([-5,-5], ylim, 'LineWidth', 2, 'Color', 'r');